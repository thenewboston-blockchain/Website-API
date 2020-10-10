# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from ..models import Contributor


class ContributorFactory(DjangoModelFactory):
    display_name = factory.Faker('name')
    github_username = factory.Faker('pystr', max_chars=250)
    slack_username = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Contributor
