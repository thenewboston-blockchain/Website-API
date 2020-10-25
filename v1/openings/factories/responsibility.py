# -*- coding: utf-8 -*-
from factory import Faker
from factory.django import DjangoModelFactory

from ..models.responsibility import Responsibility


class ResponsibilityFactory(DjangoModelFactory):
    title = Faker('pystr', max_chars=250)

    class Meta:
        model = Responsibility
