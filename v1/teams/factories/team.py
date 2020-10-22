# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from v1.users.factories import UserFactory
from ..models import Team, TeamMember


class TeamFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Team

    @factory.post_generation
    def team_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                TeamMemberFactory.create_batch(extracted, team=self)


class TeamMemberFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    is_lead = factory.Faker('pybool')
    pay_per_day = factory.Faker('pyint')
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = TeamMember
