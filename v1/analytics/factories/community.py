import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.community import Community


class CommunityFactory(DjangoModelFactory):
    projects_approved = factory.Faker('pyint')
    projects_completed = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Community
