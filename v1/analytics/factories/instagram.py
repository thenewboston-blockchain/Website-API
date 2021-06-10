import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.instagram import Instagram


class InstagramFactory(DjangoModelFactory):
    account_reached = factory.Faker('pyint')
    impressions = factory.Faker('pyint')
    profile_visits = factory.Faker('pyint')
    website_taps = factory.Faker('pyint')
    content_interactions = factory.Faker('pyint')
    followers = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Instagram
