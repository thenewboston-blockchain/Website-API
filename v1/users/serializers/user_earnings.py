from rest_framework.serializers import ModelSerializer

from .user import UserSerializer
from ..models.user_earnings import UserEarnings


class UserEarningsSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = (
            'repository',
            'time_period',
            'total_amount',
            'user',
        )
        model = UserEarnings
