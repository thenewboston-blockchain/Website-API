from rest_framework import serializers

from v1.users.models.user import User
from ..models.task import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = (
            'amount',
            'completed_date',
            'user',
            'created_date',
            'modified_date',
            'pk',
            'repository',
            'title',
        )
        model = Task
        read_only_fields = 'created_date', 'modified_date'
