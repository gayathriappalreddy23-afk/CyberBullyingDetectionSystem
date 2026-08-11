from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

        elif password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

        elif User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

        elif User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "dashboard/dashboard.html"
    )