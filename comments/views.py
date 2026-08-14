import os
import pickle
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Comment
from .forms import CommentForm

# ---------------------------------------------------------------------------
# Optional: Load NLP cyberbullying detection model if available
# ---------------------------------------------------------------------------
_model = None
_vectorizer = None


def _get_model_and_vectorizer():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        model_path = os.path.join(settings.BASE_DIR, 'model', 'cyberbullying_model.pkl')
        vectorizer_path = os.path.join(settings.BASE_DIR, 'model', 'vectorizer.pkl')
        try:
            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                with open(model_path, 'rb') as f:
                    _model = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    _vectorizer = pickle.load(f)
        except Exception as e:
            print(f"[Comments] Error loading NLP model: {e}")
    return _model, _vectorizer


def _predict_toxicity(text):
    """
    Returns (prediction, status) tuple.
    prediction: 'safe' | 'harmful'
    status:     'approved' | 'flagged'
    """
    model, vectorizer = _get_model_and_vectorizer()
    if model is not None and vectorizer is not None:
        try:
            X_text = vectorizer.transform([text])
            label = model.predict(X_text)[0]
            if label == "Cyberbullying":
                return "harmful", "flagged"
            return "safe", "approved"
        except Exception as e:
            print(f"[Comments] Prediction error: {e}")

    # Keyword fallback when model is unavailable
    toxic_words = {
        'stupid', 'ugly', 'hate', 'loser', 'worthless', 'kill',
        'die', 'idiot', 'trash', 'dumb', 'jerk', 'abuse', 'bully', 'threat',
    }
    if set(text.lower().split()).intersection(toxic_words):
        return "harmful", "flagged"
    return "safe", "approved"


# ---------------------------------------------------------------------------
# Comment View: GET (render) + POST (create)
# ---------------------------------------------------------------------------
def post_comments(request, post_id):
    """
    GET:  Display all comments for a post with pagination.
    POST: Handle new comment submission with optional NLP auto-moderation.
    """
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to post a comment.')
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # NLP auto-moderation (gracefully skipped when model is unavailable)
            prediction, status = _predict_toxicity(comment.content)
            comment.prediction = prediction
            comment.status = status

            comment.save()

            if status == 'flagged':
                messages.warning(
                    request,
                    'Your comment was flagged as potentially harmful and is pending review.'
                )
            else:
                messages.success(request, 'Your comment has been posted successfully.')

            # Redirect back to where the user came from
            referer = request.META.get('HTTP_REFERER', '')
            if 'comments' in referer:
                return redirect('comments:comments', post_id=post.pk)
            return redirect('posts:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Unable to post comment. Please check your text.')
    else:
        form = CommentForm()

    # Build paginated comments list
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


# ---------------------------------------------------------------------------
# My Comments — lists ALL comments by the currently logged-in user
# ---------------------------------------------------------------------------
@login_required
def user_comments(request):
    """
    Shows a paginated list of all comments the current user has made.
    This is the destination for the sidebar 'Comments' button.
    """
    all_comments = Comment.objects.filter(
        author=request.user
    ).select_related('post', 'author').order_by('-created_at')

    paginator = Paginator(all_comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'comment_count': all_comments.count(),
    }
    return render(request, 'comments/user_comments.html', context)
