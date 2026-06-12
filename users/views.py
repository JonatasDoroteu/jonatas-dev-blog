from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileForm, UserUpdateForm


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "users/profile_edit.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })