# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

from ..models.user import User


class UserSerializer(ModelSerializer):

    class Meta:
        fields = (
            'account_number',
            'created_date',
            'display_name',
            'github_username',
            'is_email_verified',
            'modified_date',
            'pk',
            'profile_image',
            'slack_username',
        )
        model = User
        read_only_fields = (
            'created_date',
            'is_email_verified',
            'modified_date',
            'pk',
        )


class UserSerializerCreate(ModelSerializer):

    class Meta:
        fields = (
            'email',
            'password'
        )
        model = User

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserSerializerCreate, self).create(validated_data)
        return user

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password


class UserSerializerUpdate(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = (
            'created_date',
            'is_email_verified',
            'modified_date',
            'pk',
        )
