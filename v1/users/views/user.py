from smtplib import SMTPException

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.user import SecurityLinkSerializer, UserSerializer, UserSerializerCreate, UserSerializerUpdate
from ...third_party.rest_framework.permissions import AnonWrite, ReadOnly, SelfEdit, StaffDelete
from ...utils.verification import send_account_email

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('created_date').all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializerCreate(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        try:
            send_account_email(
                request,
                'thenewboston - Verify your email',
                '/users/verify')
        except (SMTPException, ConnectionError):
            return Response({'message': 'An error occurred, please retry!'}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response(
            self.get_serializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def verify(self, request, uid, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            email = force_text(urlsafe_base64_decode(uid))
            if user is not None:
                if not user.is_email_verified:
                    user.is_active = True
                    user.is_email_verified = True
                    user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response(
                    {
                        'authentication': {
                            'access_token': str(refresh_token.access_token),
                            'refresh_token': str(refresh_token)
                        },
                        'user': UserSerializer(user).data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Token is expired', 'email': email}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError):
            return Response({'message': 'An error occurred, please retry'}, status=status.HTTP_400_BAD_REQUEST)

    def generate_new_link(self, request, *args, **kwargs):
        email = request.data.get('email')
        req_type = request.data.get('req_type')
        serializer = SecurityLinkSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get(email=email)
            if req_type == 'verify':
                path = '/users/verify'
                subject = 'thenewboston - verify your account'
            send_account_email(
                request, subject,
                path)
            return Response({'mesage': 'A new link has been sent to your email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'mesage': 'User with the given email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except (SMTPException, ConnectionError):
            return Response({'mesage': 'An error occurred, please retry'}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'generate_new_link':
            permission_classes = [AnonWrite]
        elif self.action == 'destroy':
            permission_classes = [StaffDelete]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [SelfEdit]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        serializer = UserSerializerUpdate(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            self.get_serializer(user).data
        )
