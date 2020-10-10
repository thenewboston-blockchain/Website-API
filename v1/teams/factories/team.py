# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from v1.contributors.factories import ContributorFactory
from ..models import Team, TeamContributor


class TeamFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)

    @factory.post_generation
    def contributors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                TeamContributorFactory.create_batch(extracted, team=self)

    class Meta:
        model = Team


class TeamContributorFactory(DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    contributor = factory.SubFactory(ContributorFactory)

    is_lead = factory.Faker('pybool')
    pay_per_day = factory.Faker('pyint')

    class Meta:
        model = TeamContributor
