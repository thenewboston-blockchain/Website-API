import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.twitter import Twitter


class TwitterFactory(DjangoModelFactory):
    tweets = factory.Faker('pyint')
    tweet_impressions = factory.Faker('pyint')
    profile_visits = factory.Faker('pyint')
    mentions = factory.Faker('pyint')
    total_followers = factory.Faker('pyint')
    new_followers = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Twitter
