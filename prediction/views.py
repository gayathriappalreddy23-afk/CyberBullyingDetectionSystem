from django.shortcuts import render
from django.contrib import messages


def detect_view(request):
    """
    Cyberbullying Detection tool.
    GET  → renders the detection form.
    POST → validates submitted text and renders the form with results
           (actual ML prediction integration is handled by Member 3).
    """
    result = None
    submitted_text = ''

    if request.method == 'POST':
        submitted_text = request.POST.get('text', '').strip()
        if not submitted_text:
            messages.error(request, 'Please enter some text to analyze.')
        elif len(submitted_text) > 1000:
            messages.error(request, 'Text must not exceed 1000 characters.')
        else:
            # Placeholder result — real ML prediction to be integrated by Member 3
            result = {
                'text': submitted_text,
                'label': 'Pending',
                'confidence': 'N/A',
                'is_bullying': None,
            }

    context = {
        'submitted_text': submitted_text,
        'result': result,
        'recent_predictions': [],  # Will be populated once PredictionHistory model is added
    }
    return render(request, 'prediction/detect.html', context)
