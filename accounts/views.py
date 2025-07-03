from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile


def register(request):
    """User registration view"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Account created successfully! Welcome, {user.first_name}!"
            )
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def profile(request):
    """User profile view"""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "form": form,
        "user": request.user,
        "profile": request.user.profile,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def change_password(request):
    """Change password view"""
    if request.method == "POST":
        user = request.user
        current_password = request.POST.get("current_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        elif len(new_password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        else:
            user.set_password(new_password1)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect("login")

    return render(request, "accounts/change_password.html")


# Role-based access decorators
def chef_required(view_func):
    """Decorator to require chef role"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.profile.role != "chef":
            messages.error(request, "Access denied. Chef role required.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper


def manager_required(view_func):
    """Decorator to require manager role"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.profile.role not in ["manager", "chef"]:
            messages.error(request, "Access denied. Manager role required.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):
    """Decorator to require staff role"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper
