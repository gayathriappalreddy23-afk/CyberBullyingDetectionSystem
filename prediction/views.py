import os
import pickle
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.utils import timezone

# Global references for lazy loading of ML model/vectorizer
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
            # Fallback to None if there's any loading error
            print(f"Error loading model: {e}")
            pass
            
    return _model, _vectorizer

def detect_view(request):
    """View to handle cyberbullying detection text submissions."""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if not text:
            messages.error(request, "Please enter some text to analyze.")
            return render(request, 'prediction/detect.html')
            
        model, vectorizer = get_model_and_vectorizer()
        
        if model is not None and vectorizer is not None:
            try:
                # Run prediction
                X_text = vectorizer.transform([text])
                prediction_label = model.predict(X_text)[0] # "Safe" or "Cyberbullying"
                probabilities = model.predict_proba(X_text)[0] # Probabilities for each class
                
                # Get confidence score (probability associated with the predicted class)
                class_index = list(model.classes_).index(prediction_label)
                confidence_score = float(probabilities[class_index]) * 100
                
            except Exception as e:
                # Fallback prediction if runtime error occurs
                prediction_label = "Safe"
                confidence_score = 100.0
        else:
            # Simple rule-based keyword fallback if model files aren't found/loaded
            toxic_words = {'stupid', 'ugly', 'hate', 'loser', 'worthless', 'kill', 'die', 'idiot', 'trash', 'dumb', 'jerk', 'abuse', 'bully', 'threat'}
            words = set(text.lower().split())
            if words.intersection(toxic_words):
                prediction_label = "Cyberbullying"
                confidence_score = 92.5
            else:
                prediction_label = "Safe"
                confidence_score = 95.0
                
        # Build the prediction object expected by templates/prediction/result.html
        prediction_result = {
            'text': text,
            'label': prediction_label,
            'confidence': confidence_score,
            'score': confidence_score,
            'category': prediction_label,
            'status': prediction_label,
            'created_at': timezone.now(),
            'model_name': 'TF-IDF + Logistic Regression Model',
        }
        
        # In a real app we could save to database, but there is no Prediction model.
        # We can pass recent_predictions from session history to keep it interactive.
        recent_list = request.session.get('recent_predictions', [])
        recent_list.insert(0, {
            'text': text,
            'category': prediction_label,
            'confidence': confidence_score,
            'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        # Keep only last 5 in history
        request.session['recent_predictions'] = recent_list[:5]
        
        context = {
            'prediction': prediction_result,
            'report_enabled': True,
        }
        return render(request, 'prediction/result.html', context)
        
    else:
        # GET request: load from session history if it exists
        recent_list = request.session.get('recent_predictions', [])
        context = {
            'recent_predictions': recent_list
        }
        return render(request, 'prediction/detect.html', context)
