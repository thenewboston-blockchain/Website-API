from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models.community import Community
from ..models.economy import Economy
from ..models.facebook import Facebook
from ..models.instagram import Instagram
from ..models.linkedin import LinkedIn
from ..models.network import Network
from ..models.twitter import Twitter
from ..serializers.community import CommunitySerializer
from ..serializers.economy import EconomySerializer
from ..serializers.facebook import FacebookSerializer
from ..serializers.instagram import InstagramSerializer
from ..serializers.linkedin import LinkedInSerializer
from ..serializers.network import NetworkSerializer
from ..serializers.twitter import TwitterSerializer


class CommunityViewset(ListModelMixin, GenericViewSet):
    queryset = Community.objects.all().order_by('-week_ending')
    serializer_class = CommunitySerializer


class EconomyViewset(ListModelMixin, GenericViewSet):
    queryset = Economy.objects.all().order_by('-week_ending')
    serializer_class = EconomySerializer


class NetworkViewset(ListModelMixin, GenericViewSet):
    queryset = Network.objects.all().order_by('-week_ending')
    serializer_class = NetworkSerializer


class FacebookViewset(ListModelMixin, GenericViewSet):
    queryset = Facebook.objects.all().order_by('-week_ending')
    serializer_class = FacebookSerializer


class InstagramViewset(ListModelMixin, GenericViewSet):
    queryset = Instagram.objects.all().order_by('-week_ending')
    serializer_class = InstagramSerializer


class LinkedInViewset(ListModelMixin, GenericViewSet):
    queryset = LinkedIn.objects.all().order_by('-week_ending')
    serializer_class = LinkedInSerializer


class TwitterViewset(ListModelMixin, GenericViewSet):
    queryset = Twitter.objects.all().order_by('-week_ending')
    serializer_class = TwitterSerializer
