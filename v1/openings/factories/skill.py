# -*- coding: utf-8 -*-
from factory import Faker
from factory.django import DjangoModelFactory

from ..models.skill import Skill


class SkillFactory(DjangoModelFactory):
    title = Faker('pystr', max_chars=250)

    class Meta:
        model = Skill
