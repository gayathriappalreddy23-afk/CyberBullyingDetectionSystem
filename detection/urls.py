from django.urls import path
from . import views


urlpatterns = [
    path(
        "detect/",
        views.detect_comment,
        name="detect_comment"
    ),
]