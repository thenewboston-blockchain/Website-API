# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AnonWrite(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST' and request.user.is_anonymous


class IsStaffOrReadOnly(BasePermission):
    """The request is authenticated as a user and is staff, or is a read-only request"""

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_staff) or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SelfEdit(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'PATCH' and request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj


class StaffDelete(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'DELETE' and (request.user and request.user.is_staff)
