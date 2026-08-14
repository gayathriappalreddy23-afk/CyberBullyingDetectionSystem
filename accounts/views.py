from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm, RegisterForm


# ---------------------------------------------------------------------------
# Helper: Role-based redirect after successful login
# ---------------------------------------------------------------------------

def get_post_login_redirect(user):
    """
    Determines where the user should go after successful login.
    """

    if user.is_superuser:
        return "/admin/"

    elif user.is_staff:
        return "/dashboard/moderator/"

    else:
        return "/dashboard/"


# ---------------------------------------------------------------------------
# Login View
# ---------------------------------------------------------------------------

class LoginView(DjangoLoginView):
    """
    Login view using Django's built-in authentication system.
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Redirect user according to their role.
        """

        next_url = self.get_redirect_url()

        if next_url:
            return next_url

        return get_post_login_redirect(self.request.user)


# ---------------------------------------------------------------------------
# Logout View
# ---------------------------------------------------------------------------

def logout_view(request):
    """
    Logs the user out and redirects to the home page.
    """

    if request.method == "POST":
        logout(request)
        messages.success(
            request,
            "You have been signed out successfully."
        )

        return redirect("home:home")

    return redirect("home:home")


# ---------------------------------------------------------------------------
# Register View
# ---------------------------------------------------------------------------

class RegisterView(View):
    """
    User registration.
    """

    template_name = "accounts/register.html"
    form_class = RegisterForm

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(
                get_post_login_redirect(request.user)
            )

        form = self.form_class()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                f"Welcome, {user.username}! "
                "Your account has been created."
            )

            return redirect(
                get_post_login_redirect(user)
            )

        return render(
            request,
            self.template_name,
            {"form": form},
        )


# ---------------------------------------------------------------------------
# Profile View — renders authenticated user's data and their posts
# ---------------------------------------------------------------------------

@login_required
def profile_view(request):
    """User profile page — requires authentication."""
    from posts.models import Post
    from comments.models import Comment

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    post_count = user_posts.count()
    comment_count = Comment.objects.filter(author=request.user).count()

    context = {
        'posts': user_posts,
        'post_count': post_count,
        'comment_count': comment_count,
    }
    return render(request, 'accounts/profile.html', context)


# ---------------------------------------------------------------------------
# Forgot Password
# ---------------------------------------------------------------------------

def forgot_password_view(request):
    """
    User forgot password view.
    """
    return render(request, 'accounts/forgot_password.html')