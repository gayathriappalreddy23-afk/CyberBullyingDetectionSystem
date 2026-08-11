from django.shortcuts import render


def user_dashboard(request):
    """Render the user dashboard with safe fallback values for empty contexts."""
    total_posts = 0
    total_comments = 0
    safe_count = 0
    bullying_count = 0
    recent_posts = []
    recent_activities = []

    context = {
        "user": request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "safe_count": safe_count,
        "bullying_count": bullying_count,
        "recent_posts": recent_posts,
        "recent_activities": recent_activities,
    }
    return render(request, "dashboard/user_dashboard.html", context)
