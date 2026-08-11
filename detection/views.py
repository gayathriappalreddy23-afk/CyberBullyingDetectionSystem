from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Prediction


@login_required
def detect_comment(request):

    if request.method != "POST":
        return redirect("dashboard")

    comment = request.POST.get("comment", "").strip()

    if not comment:
        return redirect("dashboard")

    # TEMPORARY ML RESULT
    # We will connect the actual ML model later.

    prediction = "safe"
    confidence = 95.0

    Prediction.objects.create(
        user=request.user,
        comment=comment,
        prediction=prediction,
        confidence=confidence,
    )

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "prediction": prediction,
            "confidence": confidence,
            "submitted_comment": comment,
        },
    )