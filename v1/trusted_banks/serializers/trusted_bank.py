from rest_framework.serializers import ModelSerializer

from ..models.trusted_bank import TrustedBank


class TrustedBankSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'ip_address', 'port', 'protocol', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        model = TrustedBank
