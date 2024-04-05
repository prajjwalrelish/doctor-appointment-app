from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class AllowAnyExceptAuthenticatedListOnly(BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return request.user and request.user.is_authenticated

        return True


class IsOwnerOrAuthenticatedReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Allow authenticated users to view it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user and request.user.is_authenticated:
            return True

        return obj == request.user


class DeleteNotAllowed(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == "destroy":
            return False

        return True
