import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.network import Network


class NetworkFactory(DjangoModelFactory):
    total_nodes = factory.Faker('pyint')
    total_transactions = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Network
