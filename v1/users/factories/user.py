# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory
from thenewboston.constants.network import VERIFY_KEY_LENGTH

from ..models import User


class UserFactory(DjangoModelFactory):
    account_number = factory.Faker('pystr', max_chars=VERIFY_KEY_LENGTH)
    display_name = factory.Faker('name')
    email = factory.Faker('email')
    github_username = factory.Faker('pystr', max_chars=250)
    slack_username = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = User
