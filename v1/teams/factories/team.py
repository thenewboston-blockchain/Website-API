# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from v1.contributors.factories import ContributorFactory
from ..models import Team, TeamContributor


class TeamFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Team

    @factory.post_generation
    def contributors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                TeamContributorFactory.create_batch(extracted, team=self)


class TeamContributorFactory(DjangoModelFactory):
    contributor = factory.SubFactory(ContributorFactory)
    is_lead = factory.Faker('pybool')
    pay_per_day = factory.Faker('pyint')
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = TeamContributor
