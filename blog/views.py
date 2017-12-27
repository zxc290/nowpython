from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Comment
from markdown import markdown
from .forms import CommentForm, UserDetailForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from datetime import datetime


# Create your views here.
def index(request, cate_name=None):
    if cate_name:
        cate = get_object_or_404(Category, name=cate_name)
        posts = cate.post_set.all()
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts, 'cate_name': cate_name})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown(post.content)
    comment_list = post.comment_set.all().filter(parent=None)

    paginator = Paginator(comment_list, 5)
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
        return render(request, 'ajax_comment_list.html', {'comment_list': comment_list})


    '''评论列表单独做ajax
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # crispy指定form_action
        # form.helper.form_action = reverse('post_detail', kwargs={'pk': post.pk})
        if form.is_valid():
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
            # 重定向到新评论所在页
            return redirect('comment_page', pk=pk, page=page)
    '''
    form = CommentForm(initial={'post': post.pk})
    return render(request, 'post_detail.html', {'post': post, 'comment_list': comment_list, 'form': form})


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

''' 重写密码修改成功后重定向
class CutsomPasswordChange(PasswordChangeView):
    def get_success_url(self):
        print('陈宫')
        return '/accounts/profile'
custom_password_change = login_required(CutsomPasswordChange.as_view())
'''


@require_POST
def ajax_comment(request):
    print(request.POST.get('content'))
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
        new_point = '#c' + str(new_comment.pk)
        return JsonResponse({'msg': '评论成功!', 'new_point': new_point})
    return JsonResponse({'msg': '评论失败!'})