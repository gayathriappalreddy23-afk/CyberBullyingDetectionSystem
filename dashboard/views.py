from django.shortcuts import render
from posts.models import Post
from django.contrib.auth.models import User

def user_dashboard(request):
    """Render the user dashboard with dynamic statistics from the database."""
    user = request.user
    
    if user and user.is_authenticated:
        # User statistics
        total_posts = Post.objects.filter(author=user).count()
        safe_count = Post.objects.filter(author=user, is_flagged=False).count()
        bullying_count = Post.objects.filter(author=user, is_flagged=True).count()
        recent_posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
        
        # Calculate recent activities based on recent posts
        recent_activities = []
        for post in recent_posts[:5]:
            status_text = "flagged as bullying" if post.is_flagged else "analyzed as safe"
            recent_activities.append({
                'title': f"Created post '{post.title}' ({status_text})",
                'timestamp': post.created_at
            })
            
        # Get latest post context for NLP Analysis Card on dashboard
        latest_post = Post.objects.filter(author=user).first()
        if latest_post:
            toxic_score = 0.96 if latest_post.is_flagged else 0.04
            sentiment = "Negative" if latest_post.is_flagged else "Positive"
            confidence = "High" if latest_post.is_flagged or latest_post.toxicity_label == 'Safe' else "Medium"
        else:
            latest_post = None
            toxic_score = 0.00
            sentiment = "Neutral"
            confidence = "N/A"
    else:
        # Fallback for unauthenticated users
        total_posts = 0
        safe_count = 0
        bullying_count = 0
        recent_posts = []
        recent_activities = []
        latest_post = None
        toxic_score = 0.00
        sentiment = "Neutral"
        confidence = "N/A"
        
    total_comments = 0 # comments is currently not implemented as a model
    
    context = {
        "user": user if user and user.is_authenticated else None,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "safe_count": safe_count,
        "bullying_count": bullying_count,
        "recent_posts": recent_posts,
        "recent_activities": recent_activities,
        "latest_post": latest_post,
        "toxic_score": toxic_score,
        "sentiment": sentiment,
        "confidence": confidence,
    }
    return render(request, "dashboard/user_dashboard.html", context)

def moderator_dashboard(request):
    """Render the moderator dashboard with dynamic data."""
    flagged_content_count = Post.objects.filter(is_flagged=True).count()
    safe_content_count = Post.objects.filter(is_flagged=False).count()
    
    reports = []
    for post in Post.objects.filter(is_flagged=True)[:5]:
        reports.append({
            'id': post.id,
            'content': post.content,
            'reason': "Potential cyberbullying",
            'reported_by': post.author.username,
            'created_at': post.created_at,
        })
        
    context = {
        'flagged_content_count': flagged_content_count,
        'safe_content_count': safe_content_count,
        'under_review_count': 0,
        'pending_reports_count': flagged_content_count,
        'reviewed_today_count': safe_content_count,
        'escalated_cases_count': 0,
        'reports': reports,
    }
    return render(request, "dashboard/moderator_dashboard.html", context)

def admin_dashboard(request):
    """Render the administrator dashboard with dynamic database stats."""
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_bullying_detected = Post.objects.filter(is_flagged=True).count()
    
    reports = []
    for post in Post.objects.filter(is_flagged=True)[:5]:
        reports.append({
            'id': post.id,
            'content_type': 'Post',
            'reason': "Potential cyberbullying",
            'reported_by': post.author.username,
            'created_at': post.created_at,
        })
        
    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': 0,
        'total_bullying_detected': total_bullying_detected,
        'pending_reports_count': total_bullying_detected,
        'active_moderators': User.objects.filter(is_staff=True).count(),
        'reports': reports,
        'safe_content_count': Post.objects.filter(is_flagged=False).count(),
        'bullying_content_count': total_bullying_detected,
        'under_review_count': 0,
    }
    return render(request, "dashboard/admin_dashboard.html", context)


