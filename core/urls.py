from django.urls import path
from . import views

urlpatterns = [
    path('sobre/', views.sobre, name='sobre'),
]
