from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return validated_data['user']

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email'].lower().strip()
        user = authenticate(username=email, password=data['password'].strip())

        if not user:
            raise serializers.ValidationError('Invalid login credentials')

        if not user.is_email_verified:
            raise serializers.ValidationError('Email not verified')

        return {'user': user}
