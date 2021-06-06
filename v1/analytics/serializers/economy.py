from rest_framework.serializers import ModelSerializer

from ..models.economy import Economy


class EconomySerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'total_coins_distributed', 'total_coins_distributed_to_core_team', 'total_coins_distributed_to_faucet',
                  'total_coins_distributed_to_projects', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        model = Economy
