from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def report_list(request):
    """
    Displays the reports page.
    Shows all flagged content reports. Currently uses placeholder context
    until the Report model is implemented.
    """
    context = {
        'reports': [],           # Replace with Report.objects.all() when model exists
        'total_reports': None,
        'pending_reports': None,
        'resolved_reports': None,
        'dismissed_reports': None,
    }
    return render(request, 'reports/report.html', context)


@login_required
def analytics_view(request):
    """
    Displays the analytics dashboard page.
    Shows system-wide statistics on cyberbullying detection.
    Currently uses placeholder context until backend models are implemented.
    """
    context = {
        'total_analyzed': None,
        'safe_count': None,
        'bullying_count': None,
        'total_reports': None,
        'pending_reports': None,
        'resolved_reports': None,
        'dismissed_reports': None,
    }
    return render(request, 'reports/analytics.html', context)


@login_required
def create_report_view(request, post_id=None, comment_id=None):
    """
    Handles report submission for posts or comments.
    Template not yet implemented.
    """
    context = {
        'post_id': post_id,
        'comment_id': comment_id,
    }
    return render(request, 'reports/create_report.html', context)
