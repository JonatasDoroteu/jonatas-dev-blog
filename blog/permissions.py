from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Allow modifications only by the author or an admin user."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or obj.author == request.user)
