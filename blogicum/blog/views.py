from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.db.models import Q
from .models import Category, Post


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
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
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)