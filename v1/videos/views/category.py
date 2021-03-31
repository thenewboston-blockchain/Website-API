from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models.category import Category
from ..serializers.category import CategorySerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects\
        .order_by('created_date')\
        .all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['name'] = data['name'].lower() if isinstance(data['name'], str) else data['name']
        serializer = CategorySerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(
            self.get_serializer(category).data,
            status=status.HTTP_201_CREATED
        )
