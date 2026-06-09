from django.urls import path
from .views import signup, profile_edit

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]