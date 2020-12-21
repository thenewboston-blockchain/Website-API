# -*- coding: utf-8 -*-
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from ..models.user import User
from ..serializers.user import UpdateSelfUserSerializer, UserSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly, SelfEdit


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('created_date').all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly | SelfEdit]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        if self.kwargs[lookup_url_kwarg] == 'me' and self.request.user and self.request.user.is_authenticated:
            filter_kwargs = {self.lookup_field: self.request.user.pk}

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'update' and self.request.user and not self.request.user.is_staff:
            return UpdateSelfUserSerializer
        return super(UserViewSet, self).get_serializer_class()
