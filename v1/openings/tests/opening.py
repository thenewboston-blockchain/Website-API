# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from v1.teams.factories.team import TeamFactory
from ..factories.opening import OpeningFactory
from ..factories.responsibility import ResponsibilityFactory
from ..factories.skill import SkillFactory
from ..models.opening import Opening


def test_opening_list(api_client, django_assert_max_num_queries):
    openings = OpeningFactory.create_batch(10, responsibilities=3, skills=5, team__team_members=2)

    with django_assert_max_num_queries(5):
        r = api_client.get(reverse('opening-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(openings[0].pk),
        'created_date': serializers.DateTimeField().to_representation(openings[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(openings[0].modified_date),
        'active': openings[0].active,
        'description': openings[0].description,
        'eligible_for_task_points': openings[0].eligible_for_task_points,
        'pay_per_day': openings[0].pay_per_day,
        'reports_to': [r.pk for r in openings[0].team.team_members.filter(is_lead=True)],
        'responsibilities': [r.pk for r in openings[0].responsibilities.all()],
        'skills': [s.pk for s in openings[0].skills.all()],
        'team': openings[0].team_id,
        'title': openings[0].title,
    }


def test_opening_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    responsibilities = ResponsibilityFactory.create_batch(5)
    skills = SkillFactory.create_batch(5)
    team = TeamFactory()

    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('opening-list'),
            data={
                'active': True,
                'description': 'Cool opening',
                'eligible_for_task_points': True,
                'pay_per_day': 9001,
                'responsibilities': [responsibilities[0].pk, responsibilities[3].pk],
                'skills': [skills[2].pk, skills[4].pk],
                'team': team.pk,
                'title': 'Opening title',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'active': True,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'description': 'Cool opening',
        'eligible_for_task_points': True,
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'pay_per_day': 9001,
        'reports_to': [r.pk for r in team.team_members.filter(is_lead=True)],
        'responsibilities': [responsibilities[0].pk, responsibilities[3].pk],
        'skills': [skills[2].pk, skills[4].pk],
        'team': team.pk,
        'title': 'Opening title',
    }

    assert Opening.objects.get(pk=r.data['pk']).title == 'Opening title'


def test_opening_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    responsibilities = ResponsibilityFactory.create_batch(3)
    skills = SkillFactory.create_batch(5)
    opening = OpeningFactory(
        responsibilities=responsibilities,
        skills=skills
    )
    team = TeamFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse('opening-detail', (opening.pk,)),
            data={
                'active': True,
                'description': 'Even Cooler opening',
                'eligible_for_task_points': True,
                'pay_per_day': 10001,
                'responsibilities': [
                    responsibilities[0].pk,
                    responsibilities[1].pk,
                    responsibilities[2].pk
                ],
                'skills': [
                    skills[0].pk,
                    skills[2].pk,
                    skills[4].pk
                ],
                'team': team.pk,
                'title': 'Updated title',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(opening.pk),
        'created_date': serializers.DateTimeField().to_representation(opening.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'active': True,
        'description': 'Even Cooler opening',
        'eligible_for_task_points': True,
        'pay_per_day': 10001,
        'reports_to': [r.pk for r in team.team_members.filter(is_lead=True)],
        'responsibilities': [
            responsibilities[0].pk,
            responsibilities[1].pk,
            responsibilities[2].pk
        ],
        'skills': [
            skills[0].pk,
            skills[2].pk,
            skills[4].pk
        ],
        'team': team.pk,
        'title': 'Updated title',
    }

    assert Opening.objects.get(pk=str(opening.pk)).title == 'Updated title'


def test_opening_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    opening = OpeningFactory(responsibilities=1, skills=1)

    r = api_client.delete(reverse('opening-detail', (opening.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Opening.objects.filter(pk=str(opening.pk)).first() is None


def test_opening_anon_post(api_client):
    r = api_client.post(reverse('opening-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_opening_anon_patch(api_client):
    opening = OpeningFactory(responsibilities=1, skills=1)

    r = api_client.post(reverse('opening-detail', (opening.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_opening_anon_delete(api_client):
    opening = OpeningFactory(responsibilities=1, skills=1)

    r = api_client.delete(reverse('opening-detail', (opening.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
