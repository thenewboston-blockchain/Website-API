# -*- coding: utf-8 -*-
from factory import Faker
from factory.django import DjangoModelFactory

from ..models import Category


class CategoryFactory(DjangoModelFactory):
    title = Faker('pystr', max_chars=250)

    class Meta:
        model = Category
