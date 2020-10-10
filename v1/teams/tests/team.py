# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from v1.contributors.factories import ContributorFactory
from ..factories import TeamFactory
from ..models import Team


def test_team_list(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, contributors=5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('team-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'title': teams[0].title,
        'contributors_meta': [{
            'contributor': c.contributor_id,
            'is_lead': c.is_lead,
            'pay_per_day': c.pay_per_day,
            'created_date': serializers.DateTimeField().to_representation(c.created_date),
            'modified_date': serializers.DateTimeField().to_representation(c.modified_date),
        } for c in teams[0].teamcontributor_set.all()],
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
    }


def test_team_contributors_empty_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('team-list'), data={
            'title': 'Star team',
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'title': 'Star team',
        'contributors_meta': [],
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }
    assert Team.objects.get(pk=r.data['pk']).title == 'Star team'


def test_team_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributors = ContributorFactory.create_batch(5)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('team-list'), data={
            'title': 'Star team',
            'contributors_meta': [
                {
                    'contributor': contributors[1].pk,
                    'is_lead': True,
                    'pay_per_day': 19001
                },
                {
                    'contributor': contributors[3].pk,
                    'is_lead': False,
                    'pay_per_day': 9001
                }
            ],
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'title': 'Star team',
        'contributors_meta': [
            {
                'contributor': contributors[1].pk,
                'is_lead': True,
                'pay_per_day': 19001,
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
            },
            {
                'contributor': contributors[3].pk,
                'is_lead': False,
                'pay_per_day': 9001,
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
            }
        ],
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }
    assert Team.objects.get(pk=r.data['pk']).title == 'Star team'


def test_team_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributor = ContributorFactory()
    team = TeamFactory(contributors=2)

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('team-detail', (team.pk,)), data={
            'title': 'Star team',
            'contributors_meta': [
                {
                    'contributor': contributor.pk,
                    'is_lead': False,
                    'pay_per_day': 9001
                },
                {
                    'contributor': team.teamcontributor_set.all()[1].contributor_id,
                    'is_lead': True,
                    'pay_per_day': 19001
                }
            ]
        }, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(team.pk),
        'title': 'Star team',
        'contributors_meta': [
            {
                'contributor': contributor.pk,
                'is_lead': False,
                'pay_per_day': 9001,
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
            },
            {
                'contributor': team.teamcontributor_set.all()[1].contributor_id,
                'is_lead': True,
                'pay_per_day': 19001,
                'created_date': serializers.DateTimeField().to_representation(
                    team.teamcontributor_set.all()[1].created_date),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
            },
        ],

        'created_date': serializers.DateTimeField().to_representation(team.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Team.objects.get(pk=str(team.pk)).title == 'Star team'


def test_team_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    team = TeamFactory(contributors=2)

    r = api_client.delete(reverse('team-detail', (team.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Team.objects.filter(pk=str(team.pk)).first() is None


def test_opening_anon_post(api_client):
    r = api_client.post(reverse('team-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_team_anon_patch(api_client):
    team = TeamFactory()

    r = api_client.post(reverse('team-detail', (team.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_team_anon_delete(api_client):
    team = TeamFactory()

    r = api_client.delete(reverse('team-detail', (team.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
