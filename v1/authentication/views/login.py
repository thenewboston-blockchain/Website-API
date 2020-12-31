from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from v1.users.serializers.user import UserSerializer
from ..serializers.login import LoginSerializer

User = get_user_model()


class LoginView(APIView):

    @staticmethod
    def post(request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)

        return Response(
            {
                'authentication': {
                    'access_token': str(refresh_token.access_token),
                    'refresh_token': str(refresh_token)
                },
                'user': UserSerializer(user).data,
            },

        )
