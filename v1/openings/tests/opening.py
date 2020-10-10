# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories import OpeningFactory
from ..models import Opening
from ...meta.factories import CategoryFactory, ResponsibilityFactory, SkillFactory
from ...teams.factories import ContributorFactory


def test_opening_list(api_client, django_assert_max_num_queries):
    openings = OpeningFactory.create_batch(10, categories=2, skills=5, responsibilities=3, reports_to=1)

    with django_assert_max_num_queries(5):
        r = api_client.get(reverse('opening-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(openings[0].pk),
        'title': openings[0].title,
        'description': openings[0].description,
        'pay_per_day': openings[0].pay_per_day,
        'eligible_for_task_points': openings[0].eligible_for_task_points,
        'active': openings[0].active,
        'reports_to': [r.pk for r in openings[0].reports_to.all()],
        'categories': [c.pk for c in openings[0].categories.all()],
        'responsibilities': [r.pk for r in openings[0].responsibilities.all()],
        'skills': [s.pk for s in openings[0].skills.all()],
        'created_date': serializers.DateTimeField().to_representation(openings[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(openings[0].modified_date),
    }


def test_opening_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    categories = CategoryFactory.create_batch(5)
    skills = SkillFactory.create_batch(5)
    responsibilities = ResponsibilityFactory.create_batch(5)
    contributors = ContributorFactory.create_batch(5)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('opening-list'), data={
            'title': 'Opening title',
            'description': 'Cool opening',
            'pay_per_day': 9001,
            'eligible_for_task_points': True,
            'active': True,
            'reports_to': [contributors[1].pk, contributors[3].pk],
            'categories': [categories[1].pk, categories[4].pk],
            'responsibilities': [responsibilities[0].pk, responsibilities[3].pk],
            'skills': [skills[2].pk, skills[4].pk]
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'title': 'Opening title',
        'description': 'Cool opening',
        'pay_per_day': 9001,
        'eligible_for_task_points': True,
        'active': True,
        'reports_to': [contributors[1].pk, contributors[3].pk],
        'categories': [categories[1].pk, categories[4].pk],
        'responsibilities': [responsibilities[0].pk, responsibilities[3].pk],
        'skills': [skills[2].pk, skills[4].pk],
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Opening.objects.get(pk=r.data['pk']).title == 'Opening title'


def test_opening_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    skills = SkillFactory.create_batch(5)
    contributor1 = ContributorFactory()
    contributor2 = ContributorFactory()
    opening = OpeningFactory(categories=2, skills=5, responsibilities=3, reports_to=[contributor1, contributor2])

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('opening-detail', (opening.pk,)), data={
            'title': 'Updated title',
            'description': 'Even Cooler opening',
            'pay_per_day': 10001,
            'eligible_for_task_points': True,
            'active': True,
            'reports_to': [contributor1.pk],
            'categories': [opening.categories.all()[0].pk, opening.categories.all()[1].pk],
            'responsibilities': [opening.responsibilities.all()[0].pk,
                                 opening.responsibilities.all()[1].pk,
                                 opening.responsibilities.all()[2].pk],
            'skills': [skills[0].pk, skills[2].pk, skills[4].pk]
        }, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(opening.pk),
        'title': 'Updated title',
        'description': 'Even Cooler opening',
        'pay_per_day': 10001,
        'eligible_for_task_points': True,
        'active': True,
        'reports_to': [contributor1.pk],
        'categories': [opening.categories.all()[0].pk, opening.categories.all()[1].pk],
        'responsibilities': [opening.responsibilities.all()[0].pk,
                             opening.responsibilities.all()[1].pk,
                             opening.responsibilities.all()[2].pk],
        'skills': [skills[0].pk, skills[2].pk, skills[4].pk],
        'created_date': serializers.DateTimeField().to_representation(opening.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Opening.objects.get(pk=str(opening.pk)).title == 'Updated title'


def test_opening_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    opening = OpeningFactory(categories=1, skills=1, responsibilities=1)

    r = api_client.delete(reverse('opening-detail', (opening.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Opening.objects.filter(pk=str(opening.pk)).first() is None


def test_opening_anon_post(api_client):
    r = api_client.post(reverse('opening-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_opening_anon_patch(api_client):
    opening = OpeningFactory(categories=1, skills=1, responsibilities=1)

    r = api_client.post(reverse('opening-detail', (opening.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_opening_anon_delete(api_client):
    opening = OpeningFactory(categories=1, skills=1, responsibilities=1)

    r = api_client.delete(reverse('opening-detail', (opening.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
