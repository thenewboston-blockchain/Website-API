import factory
from factory.django import DjangoModelFactory

from v1.users.factories.user import UserFactory
from ..models.task import Task


class TaskFactory(DjangoModelFactory):
    amount = factory.Faker('pyint')
    user = factory.SubFactory(UserFactory)
    repository = factory.Faker('pystr', max_chars=250)
    title = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Task
