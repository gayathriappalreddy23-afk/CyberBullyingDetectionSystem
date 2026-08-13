from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "comment",
        "prediction",
        "confidence",
        "created_at",
    )

    list_filter = (
        "prediction",
        "created_at",
    )

    search_fields = (
        "user__username",
        "comment",
    )

    readonly_fields = (
        "created_at",
    )

    +