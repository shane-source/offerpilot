from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from .forms import RegisterForm, LoginForm

User = get_user_model()


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            full_name = form.cleaned_data.get("full_name", "").strip()
            password = form.cleaned_data["password"]

            # ✅ prevent duplicate email
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, "That email is already registered. Please login.")
                return redirect("/login/")

            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
            )
            login(request, user)
            return redirect("/board/")

        # ✅ show exact error to you
        messages.error(request, f"Fix these: {form.errors.as_json()}")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data["user"])
            return redirect("/board/")
        messages.error(request, "Login failed. Check email/password.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")
