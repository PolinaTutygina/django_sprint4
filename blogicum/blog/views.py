from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse
from django.db.models import Q
from .models import Category, Post
from .forms import PostForm
from django.core.paginator import Paginator


User = get_user_model()


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)  # 10 публикаций на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    exclusion_condition = (
        Q(pub_date__gt=now())
        | Q(is_published=False)
        | Q(category__is_published=False)
    )
    post = get_object_or_404(
        Post.objects.exclude(exclusion_condition),
        pk=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


def create_post(request):
    template = 'blog/create.html'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, template, context)


def edit_post(request, id):
    template = 'blog/create.html'
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, template, context)


def delete_post(request, id):
    template = 'blog/create.html'
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'form': PostForm(instance=post)}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(
        author=user,
        is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def edit_profile(request):
    template = 'blog/user.html'
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, template, context)
