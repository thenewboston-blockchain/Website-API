# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    """The request is authenticated as a user and is staff, or is a read-only request"""

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or (request.user and request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class SelfEdit(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PATCH' and request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj
