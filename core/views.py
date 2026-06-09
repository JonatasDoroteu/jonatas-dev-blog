from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from blog.models import Category, Post


def home(request):
    featured_posts = Post.objects.select_related('category', 'author').prefetch_related('tags').order_by('-created_at')[:6]
    categories = Category.objects.order_by('name')[:6]
    total_posts = Post.objects.count()
    return render(request, "core/home.html", {
        "featured_posts": featured_posts,
        "categories": categories,
        "total_posts": total_posts,
    })


def profile_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    return render(request, 'core/profile.html', {
        'profile_user': user,
        'profile': profile,
    })
