from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Discussion'),
        ('cyber_safety', 'Cyber Safety & Advice'),
        ('experience', 'Personal Experience & Story'),
        ('question', 'Question / Support Request'),
        ('resource', 'Resource Sharing'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, help_text="Enter a clear, descriptive title.")
    content = models.TextField(help_text="Write your post content responsibly.")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    
    # Toxicity & Moderation fields (updated by AI prediction system)
    is_flagged = models.BooleanField(default=False)
    toxicity_label = models.CharField(max_length=50, default='Safe')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"
