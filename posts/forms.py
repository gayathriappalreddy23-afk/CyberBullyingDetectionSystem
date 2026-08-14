from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating community posts.
    The author and moderation fields are handled strictly by the Django backend.
    """
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Enter post title (max 200 characters)',
                'maxlength': '200',
                'id': 'id_title',
                'autocomplete': 'off',
                'required': True,
                'aria-label': 'Post Title',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select auth-input',
                'id': 'id_category',
                'required': True,
                'aria-label': 'Category',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Share your thoughts responsibly. Respectful and constructive dialogue is encouraged.',
                'rows': 6,
                'id': 'id_content',
                'required': True,
                'aria-label': 'Post Content',
            }),
        }
