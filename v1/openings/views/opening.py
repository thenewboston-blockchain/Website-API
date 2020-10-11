# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models import Opening
from ..serializers import OpeningSerializer, OpeningSerializerWrite


class OpeningViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Opening.objects \
        .select_related() \
        .prefetch_related('reports_to', 'responsibilities', 'skills') \
        .order_by('created_date') \
        .all()
    serializer_class = OpeningSerializer
    serializer_write_class = OpeningSerializerWrite
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_write_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        opening = serializer.save()

        return Response(
            self.get_serializer(opening).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_write_class(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        opening = serializer.save()

        return Response(
            self.get_serializer(opening).data
        )
