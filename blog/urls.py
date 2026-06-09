from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_update, name='post_update'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    path('ajax/create-category/', views.ajax_create_category, name='ajax_create_category'),
    path('ajax/create-tag/', views.ajax_create_tag, name='ajax_create_tag'),
]