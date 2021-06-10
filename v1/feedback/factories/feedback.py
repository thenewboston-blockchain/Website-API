import factory
from factory.django import DjangoModelFactory

from ..models.feedback import Feedback


class FeedbackFactory(DjangoModelFactory):
    name = factory.Faker('pystr')
    email = factory.Faker('email')
    message = factory.Faker('text')

    class Meta:
        model = Feedback
