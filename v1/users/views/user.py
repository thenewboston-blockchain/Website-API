# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet

from ..models.user import User
from ..serializers.user import UpdateSelfUserSerializer, UserSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly, SelfEdit


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('created_date').all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly | SelfEdit]

    def get_serializer_class(self):
        if self.action == 'update' and self.request.user and not self.request.user.is_staff:
            return UpdateSelfUserSerializer
        return super(UserViewSet, self).get_serializer_class()
