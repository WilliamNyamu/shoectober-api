from rest_framework import permissions


class IsCreatororReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the creator to edit or delete a product
    """
    def has_object_permission(self, request, view, obj):
        # If it is a GET method, then just return true and give the person access
        if request.method in permissions.SAFE_METHODS:
            return True
        # If it is an UNSAFE method like POST, PATCH, DELETE etc, ensure this is enforced.
        return obj.creator == request.user

class IsAuthororReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the review author to edit or delete a review
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user