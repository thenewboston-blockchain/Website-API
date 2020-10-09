# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from ..models import Opening
from ...meta.factories import CategoryFactory, ResponsibilityFactory, SkillFactory


class OpeningFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)
    description = factory.Faker('text', max_nb_chars=1024)
    pay_per_day = factory.Faker('pyint')
    eligible_for_task_points = factory.Faker('pybool')
    active = factory.Faker('pybool')

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for c in range(extracted):
                    self.categories.add(CategoryFactory())
            else:
                for category in extracted:
                    self.categories.add(category)

    @factory.post_generation
    def responsibilities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for r in range(extracted):
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
                for s in range(extracted):
                    self.skills.add(SkillFactory())
            else:
                for skill in extracted:
                    self.skills.add(skill)

    class Meta:
        model = Opening
