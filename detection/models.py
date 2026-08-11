from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Prediction(models.Model):
    PREDICTION_CHOICES = [
        ("safe", "Safe"),
        ("bullying", "Bullying"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    comment = models.TextField()

    prediction = models.CharField(
        max_length=20,
        choices=PREDICTION_CHOICES
    )

    confidence = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"