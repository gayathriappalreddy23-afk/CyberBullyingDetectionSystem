from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('pending', 'Pending Review'),
        ('flagged', 'Flagged'),
        ('removed', 'Removed'),
    )

    PREDICTION_CHOICES = (
        ('safe', 'Safe'),
        ('harmful', 'Potentially Harmful'),
        ('under_review', 'Under Review'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    prediction = models.CharField(max_length=20, choices=PREDICTION_CHOICES, default='safe')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
