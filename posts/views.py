from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
from .forms import PostForm


def post_list(request):
    """
    Render community posts with server-side search, category filter, and pagination.
    """
    posts_queryset = Post.objects.all().select_related('author')
    
    # 1. Search Query Filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        posts_queryset = posts_queryset.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    # 2. Category Filter
    selected_category = request.GET.get('category', '').strip()
    if selected_category:
        posts_queryset = posts_queryset.filter(category=selected_category)

    # 3. Server-side Pagination (6 posts per page)
    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_category': selected_category,
        'categories': Post.CATEGORY_CHOICES,
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def create_post(request):
    """
    Handles secure post creation.
    Associates post with request.user automatically on the backend.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been published successfully.')
            return redirect('posts:post_list')
        else:
            messages.error(request, 'Please correct the errors in the form below.')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


def post_detail(request, pk):
    """
    Render individual post details along with comments.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author').all()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_count': comments.count(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def edit_post(request, pk):
    """
    Edit an existing post (ownership verified server-side).
    """
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated.')
            return redirect('posts:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    """
    Handles post deletion (ownership verified server-side).
    """
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted.')
    return redirect('posts:post_list')
