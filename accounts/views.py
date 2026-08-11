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
# Profile View
# ---------------------------------------------------------------------------

@login_required
def profile_view(request):
    """
    User profile page.
    """

    return render(
        request,
        "accounts/profile.html"
    )