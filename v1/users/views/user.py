# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models.user import User
from ..serializers.user import UserSerializer, UserSerializerCreate, UserSerializerUpdate
from ...third_party.rest_framework.permissions import AnonWrite, ReadOnly, SelfEdit, StaffDelete


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('created_date').all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializerCreate(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            self.get_serializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AnonWrite]
        elif self.action == 'destroy':
            permission_classes = [StaffDelete]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [SelfEdit]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        serializer = UserSerializerUpdate(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            self.get_serializer(user).data
        )
