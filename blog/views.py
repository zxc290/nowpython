from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Comment
from markdown import markdown
from .forms import CommentForm, UserDetailForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from . import handlers


# Create your views here.
def index(request, cate_name=None):
    if cate_name:
        cate = get_object_or_404(Category, name=cate_name)
        posts = cate.post_set.all()
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts, 'cate_name': cate_name})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.content = markdown(post.content, extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
    comment_list = post.comment_set.all().filter(parent=None)

    paginator = Paginator(comment_list, 10)
    page = request.GET.get('page')
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        comment_list = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'blog/ajax_comment_list.html', {'comment_list': comment_list})
    form = CommentForm(initial={'post': post.pk})
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_list': comment_list, 'form': form})


@login_required
def account_profile(request):
    messages = []
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('资料修改成功')
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/user_detail.html', {'form': form, 'messages': messages})


@require_POST
@login_required
def ajax_comment(request):
    form = CommentForm(request.POST)
    if request.is_ajax() and form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        reply_to = form.cleaned_data['reply_to']
        # 直接回复时,reply_to为none,确保reply_to非空才能操作parent属性
        if reply_to is not None:
            # 当回复的评论不是根评论时,上级评论与新评论有共同根评论
            if reply_to.parent:
                new_comment.parent = reply_to.parent
                # 当回复了根评论时，新回复的根评论即为reply_to本身
            else:
                new_comment.parent = reply_to
        new_comment.save()
        return render(request, 'blog/ajax_comment.html', {'new_comment': new_comment})
    return JsonResponse({'msg': '评论失败!'})


def timeline(request):
    post_list = Post.objects.order_by('-pub_time')
    return render(request, 'blog/timeline.html', {'post_list': post_list})