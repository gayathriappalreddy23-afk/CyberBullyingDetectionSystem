from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User



class LoginForm(AuthenticationForm):
    """
    Extends Django's built-in AuthenticationForm.
    Uses 'username' as the login identifier (Django default).
    All password verification is handled by Django's authentication backend.
    """
    username = forms.CharField(
        label='Username',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'autofocus': True,
            'id': 'id_username',
            'aria-label': 'Username',
            'aria-required': 'true',
        })
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'id': 'id_password',
            'aria-label': 'Password',
            'aria-required': 'true',
        })
    )

    error_messages = {
        'invalid_login': (
            "Invalid username or password. Please check your credentials and try again."
        ),
        'inactive': "This account has been disabled. Please contact support.",
    }


class RegisterForm(UserCreationForm):
    """
    Standard user registration form using Django's built-in UserCreationForm.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
            'id': 'id_email',
            'aria-label': 'Email Address',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all inherited fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control auth-input'})
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
            'autofocus': True,
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ResetPasswordForm(PasswordResetForm):
    """
    Extends Django's built-in PasswordResetForm with Bootstrap styling.
    """
    email = forms.EmailField(
        label='Email Address',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your registered email address',
            'autocomplete': 'email',
            'id': 'id_email',
            'aria-label': 'Email Address',
            'aria-required': 'true',
            'autofocus': True,
        })
    )

