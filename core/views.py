from django.shortcuts import render
from blog.models import Post


def home(request):
    recent_posts = Post.objects.select_related('category', 'author').order_by('-created_at')[:4]
    from blog.models import Category
    categories = Category.objects.all()
    total_posts = Post.objects.count()
    return render(request, "core/home.html", {
        "featured_posts": recent_posts,
        "categories": categories,
        "total_posts": total_posts,
    })


def sobre(request):
    return render(request, "core/sobre.html")
