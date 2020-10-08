# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.reverse import reverse

from ..factories import CategoryFactory, ResponsibilityFactory, SkillFactory


def test_category_list(api_client, django_assert_max_num_queries):
    categories = CategoryFactory.create_batch(5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('category-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
    assert r.data[0] == {
        'pk': categories[0].pk,
        'title': categories[0].title}


def test_responsibility_list(api_client, django_assert_max_num_queries):
    responsibilities = ResponsibilityFactory.create_batch(5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('responsibility-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
    assert r.data[0] == {
        'pk': responsibilities[0].pk,
        'title': responsibilities[0].title}


def test_skill_list(api_client, django_assert_max_num_queries):
    skills = SkillFactory.create_batch(5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('skill-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
    assert r.data[0] == {
        'pk': skills[0].pk,
        'title': skills[0].title}
