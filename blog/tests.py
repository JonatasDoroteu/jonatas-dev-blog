import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Category, Post, Tag


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="author", password="password123")


@pytest.fixture
def staff_user(db):
    User = get_user_model()
    return User.objects.create_user(username="admin", password="password123", is_staff=True)


@pytest.fixture
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(username="guest", password="password123")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Backend", slug="backend")


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Django", slug="django")


@pytest.fixture
def post(db, user, category, tag):
    post = Post.objects.create(
        title="API Post",
        content="Post created for API tests.",
        author=user,
        category=category,
    )
    post.tags.add(tag)
    return post


def test_post_list_returns_posts(api_client, post):
    url = reverse("post-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"]
    assert response.data["results"][0]["title"] == "API Post"


def test_post_detail_returns_single_post(api_client, post):
    url = reverse("post-detail", args=[post.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "API Post"
    assert response.data["category"]["slug"] == "backend"


def test_authenticated_user_can_create_post(api_client, user, category, tag):
    api_client.force_authenticate(user=user)
    url = reverse("post-list")
    data = {
        "title": "New API Post",
        "content": "Content from pytest.",
        "category_id": category.id,
        "tag_ids": [tag.id],
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New API Post"
    assert response.data["author"] == "author"


def test_unauthenticated_user_cannot_create_post(api_client, category, tag):
    url = reverse("post-list")
    data = {
        "title": "Unauthorized Post",
        "content": "Should fail",
        "category_id": category.id,
        "tag_ids": [tag.id],
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_author_can_update_own_post(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse("post-detail", args=[post.pk])
    response = api_client.patch(url, {"title": "Updated API Post"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated API Post"


def test_other_user_cannot_update_post(api_client, other_user, post):
    api_client.force_authenticate(user=other_user)
    url = reverse("post-detail", args=[post.pk])
    response = api_client.patch(url, {"title": "Hacked Title"}, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_user_can_update_any_post(api_client, staff_user, post):
    api_client.force_authenticate(user=staff_user)
    url = reverse("post-detail", args=[post.pk])
    response = api_client.patch(url, {"title": "Admin Updated Title"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Admin Updated Title"


def test_filter_posts_by_category(api_client, post):
    url = reverse("post-list") + "?category__slug=backend"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"]
    assert response.data["results"][0]["category"]["slug"] == "backend"
