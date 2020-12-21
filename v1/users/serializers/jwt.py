# -*- coding: utf-8 -*-
from rest_framework import serializers


class TNBJWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
