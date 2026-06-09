from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog.api.views import CategoryViewSet, TagViewSet, PostViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
