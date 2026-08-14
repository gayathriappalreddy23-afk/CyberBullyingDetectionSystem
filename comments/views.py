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

_model = None
_vectorizer = None

def get_model_and_vectorizer():
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
            print(f"Error loading model in comments: {e}")
            pass
            
    return _model, _vectorizer

def predict_toxicity(text):
    model, vectorizer = get_model_and_vectorizer()
    if model is not None and vectorizer is not None:
        try:
            X_text = vectorizer.transform([text])
            prediction_label = model.predict(X_text)[0] # "Safe" or "Cyberbullying"
            if prediction_label == "Cyberbullying":
                return "harmful", "flagged"
            else:
                return "safe", "approved"
        except Exception as e:
            print(f"Prediction error in comments: {e}")
            pass
            
    # Fallback keyword list if model fails to load
    toxic_words = {'stupid', 'ugly', 'hate', 'loser', 'worthless', 'kill', 'die', 'idiot', 'trash', 'dumb', 'jerk', 'abuse', 'bully', 'threat'}
    words = set(text.lower().split())
    if words.intersection(toxic_words):
        return "harmful", "flagged"
    return "safe", "approved"

def post_comments(request, post_id):
    """
    GET: Render all comments for a post, with pagination.
    POST: Handle posting a new comment with automatic AI moderation.
    """
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # NLP Toxicity evaluation
            prediction, status = predict_toxicity(comment.content)
            comment.prediction = prediction
            comment.status = status
            
            comment.save()
            
            if status == "flagged":
                messages.warning(request, "Your comment was flagged by the system as potentially harmful and is pending review.")
            else:
                messages.success(request, "Comment posted successfully.")
                
            # Smart Redirect based on referer
            referer = request.META.get('HTTP_REFERER', '')
            if 'comments' in referer:
                return redirect('comments:comments', post_id=post.id)
            else:
                return redirect('posts:post_detail', pk=post.id)
        else:
            messages.error(request, "Error posting comment. Please ensure the comment length is valid.")
            
    # GET (or invalid POST): Query, Paginate, and Display Comments
    # Sort with oldest first or newest first. Template loops over them.
    # Let's show newest comments first (ordering is already ['-created_at'] in Meta)
    comments_list = post.comments.all()
    comment_count = comments_list.count()
    
    paginator = Paginator(comments_list, 5) # 5 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'post': post,
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'comment_count': comment_count,
        'form': CommentForm(),
    }
    return render(request, 'comments/comments.html', context)
