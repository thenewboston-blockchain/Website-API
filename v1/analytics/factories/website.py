import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.website import Website


class WebsiteFactory(DjangoModelFactory):
    users = factory.Faker('pyint')
    sessions = factory.Faker('pyint')
    bounce_rate = factory.Faker('pyfloat')
    session_duration = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Website
