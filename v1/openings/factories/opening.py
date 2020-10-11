# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from v1.teams.factories import TeamFactory
from .responsibility import ResponsibilityFactory
from .skill import SkillFactory
from ..models import Opening
from ...contributors.factories import ContributorFactory


class OpeningFactory(DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    active = factory.Faker('pybool')
    description = factory.Faker('text', max_nb_chars=1024)
    eligible_for_task_points = factory.Faker('pybool')
    pay_per_day = factory.Faker('pyint')
    title = factory.Faker('pystr', max_chars=250)

    @factory.post_generation
    def reports_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.reports_to.add(ContributorFactory())
            else:
                for reports_to in extracted:
                    self.reports_to.add(reports_to)

    @factory.post_generation
    def responsibilities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.responsibilities.add(ResponsibilityFactory())
            else:
                for responsibility in extracted:
                    self.responsibilities.add(responsibility)

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.skills.add(SkillFactory())
            else:
                for skill in extracted:
                    self.skills.add(skill)

    class Meta:
        model = Opening
