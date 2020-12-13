# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from ..models.repository import Repository


class RepositoryFactory(DjangoModelFactory):
    url = factory.Faker('url')
    display_name = factory.Faker('name')

    class Meta:
        model = Repository
