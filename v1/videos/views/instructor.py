from config.helpers.cache import CachedModelViewSet
from ..models.instructor import Instructor
from ..serializers.instructor import InstructorSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class InstructorViewSet(CachedModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsStaffOrReadOnly]
