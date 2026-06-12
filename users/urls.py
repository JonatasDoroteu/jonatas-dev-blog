from django.urls import path
from .views import signup, profile_edit, profile_view

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup/", signup, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]