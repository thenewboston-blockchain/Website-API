from rest_framework.serializers import ModelSerializer

from ..models.network import Network


class NetworkSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'total_nodes', 'total_transactions', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        model = Network
