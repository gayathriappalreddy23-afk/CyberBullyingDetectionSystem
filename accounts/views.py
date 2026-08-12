from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView as DjangoLoginView

from .forms import LoginForm, RegisterForm


# ---------------------------------------------------------------------------
# Helper: Role-based redirect after successful login
# ---------------------------------------------------------------------------
def get_post_login_redirect(user):
    """
    Determines the correct redirect URL after a successful login
    based on Django's built-in permission flags.

    - Superuser  → Django Admin (or admin dashboard if one is built)
    - Staff      → Moderator dashboard
    - Regular    → User dashboard

    SECURITY: This is evaluated server-side on the authenticated user object.
    The frontend never controls this decision.
    """
    if user.is_superuser:
        return '/admin/'
    elif user.is_staff:
        return '/dashboard/moderator/'
    else:
        return '/dashboard/'


# ---------------------------------------------------------------------------
# Login View — extends Django's LoginView for full CSRF + session handling
# ---------------------------------------------------------------------------
class LoginView(DjangoLoginView):
    """
    Secure login view using Django's built-in LoginView.
    - Uses AuthenticationForm (via LoginForm) for credential validation.
    - Session management, CSRF protection, and brute-force timing-safe
      comparison are all handled by Django's authentication framework.
    - Role-based redirect is resolved server-side after authentication.
    """
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True   # Redirect if already logged in

    def get_success_url(self):
        """Override to implement role-based server-side redirect."""
        # Honour ?next= parameter first (Django standard), then role redirect
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
    Uses POST to protect against CSRF-based logout attacks.
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
    return redirect('home:home')


# ---------------------------------------------------------------------------
# Register View
# ---------------------------------------------------------------------------
class RegisterView(View):
    """
    Standard user registration using Django's UserCreationForm wrapper.
    """
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(get_post_login_redirect(request.user))
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect(get_post_login_redirect(user))
        return render(request, self.template_name, {'form': form})


# ---------------------------------------------------------------------------
@login_required
def profile_view(request):
    """User profile page — requires authentication."""
    from posts.models import Post
    from comments.models import Comment
    user_posts = Post.objects.filter(author=request.user)
    post_count = user_posts.count()
    comment_count = Comment.objects.filter(author=request.user).count()
    
    context = {
        'posts': user_posts,
        'post_count': post_count,
        'comment_count': comment_count,
    }
    return render(request, 'accounts/profile.html', context)



# ---------------------------------------------------------------------------
# Forgot Password (uses Django's built-in password reset URLs)
# ---------------------------------------------------------------------------
def forgot_password_view(request):
    """
    Entry point for the forgot-password flow.
    Django's built-in password reset is wired through
    django.contrib.auth.views — this view renders the intro page.
    """
    return render(request, 'accounts/forgot_password.html')
