# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models.email import Email


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'subscribed',
            'created_at',
            'modified_at',
        )
        model = Email
        read_only_fields = 'created_at', 'modified_at'
