from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings

from .models import Post, Group, User
from .forms import PostForm


def get_paginator_context(queryset, page_number, page_size=settings.PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': paginator.get_page(page_number),
    }


def index(request): 
    context = get_paginator_context(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    context = {
        'group': group,
        'posts': posts
    }
    context.update(get_paginator_context(group.posts.all(), request))
    return render(request, template, context)


def profile(request, username):
    profile_auth = get_object_or_404(User, username=username)
    post_auth = profile_auth.posts.all()
    context = {
        'post_auth': post_auth,
        'profile_auth': profile_auth
    }
    context.update(get_paginator_context(profile_auth.posts.all(), request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    user_posts = Post.objects.filter(pk=post_id)
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=post.author).count()
    context = {
        'user_posts': user_posts,
        'post': post,
        'count': count
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text_variable = form.cleaned_data['text']
            group_variable = form.cleaned_data['group']
            Post.objects.create(text=text_variable, group=group_variable,
                                author=request.user)
            return redirect(f'/profile/{request.user}/', username=request.user)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
    is_edit = True
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
        return render(request, 'posts/create_post.html', {'form': form})
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': is_edit})
