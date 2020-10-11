# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from v1.contributors.factories import ContributorFactory
from ..models import Task


class TaskFactory(DjangoModelFactory):
    amount = factory.Faker('pyint')
    contributor = factory.SubFactory(ContributorFactory)
    repository = factory.Faker('pystr', max_chars=250)
    title = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Task
