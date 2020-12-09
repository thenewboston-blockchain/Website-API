# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

# from v1.users.factories.user import UserFactory
from ..models.repository import Repository


class RepositoryFactory(DjangoModelFactory):
    url = factory.Faker('pystr', max_chars=80)
    display_name = factory.Faker('name')

    class Meta:
        model = Repository
