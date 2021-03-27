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
