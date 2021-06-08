import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.economy import Economy


class EconomyFactory(DjangoModelFactory):
    total_coins_distributed = factory.Faker('pyint')
    total_coins_distributed_to_core_team = factory.Faker('pyint')
    total_coins_distributed_to_faucet = factory.Faker('pyint')
    total_coins_distributed_to_projects = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Economy
