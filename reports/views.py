from django.shortcuts import render

# Create your views here.

def report_list(request):
    return render(request, 'reports/report.html')

def analytics_view(request):
    return render(request, 'reports/analytics.html')

def create_report_view(request, post_id=None, comment_id=None):
    return render(request, 'reports/create_report.html')
