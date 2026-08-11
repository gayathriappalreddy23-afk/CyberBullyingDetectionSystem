from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages


def home_view(request):
    """Public landing / home page."""
    return render(request, 'home/home.html')


def about_view(request):
    """Public about / project documentation page."""
    return render(request, 'home/about.html')


@require_http_methods(["GET", "POST"])
def contact_view(request):
    """Public contact page with form handling."""
    if request.method == 'POST':
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip()
        subject  = request.POST.get('subject', '').strip()
        category = request.POST.get('category', '').strip()
        priority = request.POST.get('priority', 'normal').strip()
        message  = request.POST.get('message', '').strip()

        # Basic server-side validation
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email or '@' not in email:
            errors.append('A valid email address is required.')
        if not subject:
            errors.append('Subject is required.')
        if not message or len(message) < 10:
            errors.append('Message must be at least 10 characters.')

        # If AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if errors:
                return JsonResponse({'success': False, 'message': ' '.join(errors)}, status=400)

            # TODO: Send email or save to database
            # For now, log to Django messages and return success
            return JsonResponse({'success': True, 'message': 'Your message has been received.'})

        # Standard POST (non-AJAX)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'home/contact.html', {
                'form_data': {
                    'name': name, 'email': email,
                    'subject': subject, 'category': category,
                    'priority': priority, 'message': message,
                }
            })

        messages.success(request, 'Your message has been sent! We\'ll get back to you within 24 hours.')
        return render(request, 'home/contact.html')

    return render(request, 'home/contact.html')
