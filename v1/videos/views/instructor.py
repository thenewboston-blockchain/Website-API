from rest_framework.viewsets import ModelViewSet

from ..models.instructor import Instructor
from ..serializers.instructor import InstructorSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsStaffOrReadOnly]
