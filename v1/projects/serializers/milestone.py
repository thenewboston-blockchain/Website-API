from rest_framework.serializers import ModelSerializer

from ..models.milestone import Milestone


class MilestoneSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Milestone
        read_only_fields = ('created_date', 'modified_date')
