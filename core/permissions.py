"""
Custom permissions for the healthcare backend.
"""

from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Permission that checks if the requesting user is the owner of the object.
    Used for Patient resources to ensure users can only access their own patients.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the object has a created_by attribute and if it matches the request user
        return hasattr(obj, 'created_by') and obj.created_by == request.user
