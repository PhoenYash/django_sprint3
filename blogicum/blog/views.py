from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from blog.models import Post
from datetime import datetime
from django.http import Http404


def index(request):
    template_name = "blog/index.html"
    post_list = Post.objects.all().filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=datetime.now())
    ).order_by(
        '-pub_date'
    )[0:5]
    context = {"post_list": post_list}
    return render(request, template_name, context)


def post_detail(request, pk):
    template_name = "blog/detail.html"
    post = get_object_or_404(
        Post.objects.all(),
        Q(pk=pk)
        & Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=datetime.now())
    )
    context = {"post": post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = "blog/category.html"
    post_list = get_list_or_404(
        Post.objects.all(),
        (
            Q(is_published=True)
            & Q(category__slug__contains=category_slug)
            & Q(pub_date__lte=datetime.now())
        )
    )
    category = post_list[0].category
    if not category.is_published:
        raise Http404
    context = {"category": category,
               "post_list": post_list}
    return render(request, template_name, context)
