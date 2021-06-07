import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.other_social import OtherSocial


class OtherSocialFactory(DjangoModelFactory):
    discord_members = factory.Faker('pyint')
    reddit_subscribers = factory.Faker('pyint')
    youtube_subscribers = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = OtherSocial
