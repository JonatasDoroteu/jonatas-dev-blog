from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Category, Tag, Post
from .forms import PostForm


# READ (lista)
def post_list(request):
    posts = Post.objects.select_related('category', 'author').prefetch_related('tags').all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')
    selected_category = request.GET.get('category')
    if selected_category:
        posts = posts.filter(category__slug=selected_category)

    featured_posts = posts[:4]

    return render(request, "blog/post_list.html", {
        "posts": posts,
        "categories": categories,
        "featured_posts": featured_posts,
        "selected_category": selected_category,
    })


# READ (detalhe)
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "blog/post_detail.html", {"post": post})


# CREATE
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


# UPDATE
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form})


# DELETE
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, "blog/post_confirm_delete.html", {"post": post})


@login_required
@require_POST
def ajax_create_category(request):
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name required'}, status=400)

    obj, created = Category.objects.get_or_create(name=name)
    return JsonResponse({'id': obj.id, 'name': obj.name, 'slug': obj.slug})


@login_required
@require_POST
def ajax_create_tag(request):
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name required'}, status=400)

    obj, created = Tag.objects.get_or_create(name=name)
    return JsonResponse({'id': obj.id, 'name': obj.name, 'slug': obj.slug})