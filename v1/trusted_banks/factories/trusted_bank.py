import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from thenewboston.constants.network import PROTOCOL_CHOICES

from ..models.trusted_bank import TrustedBank


class TrustedBankFactory(DjangoModelFactory):
    ip_address = factory.Faker('ipv4')
    port = factory.Faker('random_int', min=0, max=65535)
    protocol = FuzzyChoice([p[1] for p in PROTOCOL_CHOICES])

    class Meta:
        model = TrustedBank
