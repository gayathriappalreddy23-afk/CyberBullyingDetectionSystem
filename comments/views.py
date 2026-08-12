from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from posts.models import Post
from .models import Comment
from .forms import CommentForm


def post_comments(request, post_id):
    """
    Renders comments list and handles new comment submissions for a post.
    """
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to post a comment.')
            return redirect('accounts:login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted successfully.')
            return redirect('comments:comments', post_id=post.id)
        else:
            messages.error(request, 'Unable to post comment. Please check your text.')
    else:
        form = CommentForm()

    comments_list = post.comments.select_related('author').all()
    paginator = Paginator(comments_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post': post,
        'form': form,
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'comment_count': comments_list.count(),
    }
    return render(request, 'comments/comments.html', context)
