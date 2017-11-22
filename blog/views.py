from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, User, Category
from markdown import markdown
from .forms import RegisterForm, EditProfileForm, PostForm


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
    return render(request, 'post_detail.html', {'post': post })


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