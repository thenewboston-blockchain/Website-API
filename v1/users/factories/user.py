import factory
from factory.django import DjangoModelFactory
from thenewboston.constants.network import VERIFY_KEY_LENGTH

from .user_earnings import UserEarningsFactory
from ..models.user import User
from ..models.user_earnings import UserEarnings


class UserFactory(DjangoModelFactory):
    account_number = factory.Faker('pystr', max_chars=VERIFY_KEY_LENGTH)
    display_name = factory.Faker('name')
    email = factory.Faker('email')
    github_username = factory.Faker('pystr', max_chars=250)
    slack_username = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = User

    @factory.post_generation
    def repositories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for repository in extracted:
                for time_period in UserEarnings.TimePeriod.values:
                    UserEarningsFactory(
                        user=self,
                        repository=repository,
                        time_period=time_period,
                    )
