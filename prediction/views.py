from django.shortcuts import render

# Create your views here.

def detect_view(request):
    """View to handle cyberbullying detection."""
    return render(request, 'prediction/detect.html')
