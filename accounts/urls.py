from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import ResetPasswordForm

app_name = "accounts"

urlpatterns = [
    # Authentication
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),

    # Profile
    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),

    # Password reset - Step 1
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/forgot_password.html",
            form_class=ResetPasswordForm,
            email_template_name="accounts/emails/password_reset_email.txt",
            subject_template_name="accounts/emails/password_reset_subject.txt",
            success_url="/accounts/password-reset/sent/",
        ),
        name="forgot_password",
    ),

    # Password reset - Step 2
    path(
        "password-reset/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    # Password reset - Step 3
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),

    # Password reset - Step 4
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]