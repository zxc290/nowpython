from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, User, Category, Comment
from markdown import markdown
from .forms import RegisterForm, ReplyForm, EditProfileForm, PostForm, CommentForm
from .weather import get_city_weather

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

    # 查询天气
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    weather = get_city_weather(ip)

    return render(request, 'index.html', {'posts': posts, 'cate_name': cate_name, 'weather': weather})


def post_detail(request, pk, page=1):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown(post.content)
    comment_list = post.comment_set.all()
    for floor, comment in enumerate(comment_list):
        comment.floor = floor + 1

    comment_paginator = Paginator(comment_list, 10, 3)
    try:
        comment_list = comment_paginator.page(page)
    except PageNotAnInteger:
        comment_list = comment_paginator.page(1)
    except EmptyPage:
        comment_list = comment_paginator.page(comment_paginator.num_pages)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user.username
            comment.email = request.user.email
            comment.post = post
            comment.save()
            return redirect(post)
    comment_form = CommentForm()
    reply_form = ReplyForm()
    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form, 'reply_form': reply_form,
                                                'comment_list': comment_list})


def reply_to_comment(request, comment_pk):
    comment_pk = comment_pk
    comment = Comment.objects.get(pk=comment_pk)
    post = Post.objects.get(comment=comment)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = comment
            reply.name = request.user.username
            reply.save()
            return redirect(post)




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


def about_me(request):
    post = User.objects.get(username='john').post_set.get(title='关于我')
    return render(request, 'post_detail.html', {'post': post})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'user_profile.html', {'user': user, 'form': form})


def new_post(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if 'publish' in request.POST and form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def edit_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            form = PostForm(instance=request.post)
        except AttributeError:
            form = PostForm()
    return render(request, 'edit_post.html', {'form': form})