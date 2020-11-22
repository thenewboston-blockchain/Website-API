# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from ..models.email import Email


class EmailFactory(DjangoModelFactory):
    email = factory.Faker('email')
    subscribed = factory.Faker('pybool')

    class Meta:
        model = Email
