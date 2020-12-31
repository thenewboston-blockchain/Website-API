from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from v1.repositories.factories.repositories import RepositoryFactory
from ..models.user_earnings import UserEarnings


class UserEarningsFactory(DjangoModelFactory):
    user = SubFactory('v1.users.factories.user.UserFactory')

    total_amount = Faker('pyint')
    repository = SubFactory(RepositoryFactory)
    time_period = FuzzyChoice(
        UserEarnings.TimePeriod.values
    )

    class Meta:
        model = UserEarnings
