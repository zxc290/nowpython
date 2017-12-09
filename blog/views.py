from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Comment
from markdown import markdown
from .forms import RegisterForm, CommentForm, UserDetailForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request, page=1, cate_name=None):
    if cate_name:
        cate = get_object_or_404(Category, name=cate_name)
        posts = cate.post_set.all()
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts, 'cate_name': cate_name})


def post_detail(request, pk, page=1):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown(post.content)
    comment_list = post.comment_set.all().filter(parent=None)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            reply_to = comment_form.cleaned_data['reply_to']
            # 直接回复时,reply_to为none,确保reply_to非空才能操作parent属性
            if reply_to is not None:
                # 当回复的评论不是根评论时,上级评论与新评论有共同根评论
                if reply_to.parent:
                    new_comment.parent = reply_to.parent
                    # 当回复了根评论时，新回复的根评论即为reply_to本身
                else:
                    new_comment.parent = reply_to
            new_comment.save()
            return redirect(post)
    comment_form = CommentForm(initial={'post': post.pk})
    return render(request, 'post_detail.html', {'post': post, 'comment_list': comment_list, 'comment_form': comment_form })


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = RegisterForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def account_profile(request):
    messages = []
    if request.method == 'POST':
        form =UserDetailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('资料修改成功')
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/user_detail.html', {'form': form, 'messages': messages})