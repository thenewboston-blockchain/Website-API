import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.linkedin import LinkedIn


class LinkedInFactory(DjangoModelFactory):
    views = factory.Faker('pyint')
    unique_visitors = factory.Faker('pyint')
    custom_button_clicks = factory.Faker('pyint')
    reactions = factory.Faker('pyint')
    comments = factory.Faker('pyint')
    shares = factory.Faker('pyint')
    page_follow = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = LinkedIn
