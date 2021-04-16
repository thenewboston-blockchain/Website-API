from rest_framework.permissions import BasePermission, SAFE_METHODS

from v1.teams.models.team import CoreTeam, ProjectTeam
from v1.teams.models.team_member import CoreMember, ProjectMember


class AnonWrite(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_anonymous and request.method == 'POST'


class IsStaffOrReadOnly(BasePermission):
    """The request is authenticated as a user and is staff, or is a read-only request"""

    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUserOrReadOnly(BasePermission):
    """The request is authenticated as a user and is superuser or is a read-only request"""

    def has_permission(self, request, view):
        return (request.user and request.user.is_superuser) or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SelfEdit(BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated) and request.method == 'PATCH'

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj


class StaffDelete(BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) and request.method == 'DELETE'


class IsSuperUserOrTeamLead(BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_superuser) or self.has_object_permission

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, CoreTeam):
            members = CoreMember.objects.filter(user=request.user, core_team=obj)
            is_lead = is_team_lead(members)
        elif isinstance(obj, ProjectTeam):
            members = ProjectMember.objects.filter(user=request.user, project_team=obj)
            is_lead = is_team_lead(members)
        else:
            if isinstance(obj, CoreMember):
                members = CoreMember.objects.filter(user=request.user, core_team=obj.core_team)
                is_lead = is_team_lead(members)
            elif isinstance(obj, ProjectMember):
                members = ProjectMember.objects.filter(user=request.user, project_team=obj.project_team)
                is_lead = is_team_lead(members)
            else:
                is_lead = False
        return is_lead


def is_team_lead(members):
    if len(members) > 0:
        is_lead = members[0].is_lead
    else:
        is_lead = False
    return is_lead
