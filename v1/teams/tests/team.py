from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from v1.users.factories.user import UserFactory
from ..factories.team import CoreTeamFactory, ProjectTeamFactory, TeamFactory
from ..models.team import CoreTeam, ProjectTeam, Team


def test_teams_list(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(3):
        r = api_client.get(reverse('team-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
        'team_members_meta': [{
            'team': team_member.team_id,
            'user': team_member.user_id,
            'is_lead': team_member.is_lead,
            'pay_per_day': team_member.pay_per_day,
            'job_title': team_member.job_title,
            'created_date': serializers.DateTimeField().to_representation(team_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(team_member.modified_date),
        } for team_member in teams[0].team_members.order_by('created_date').all()],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'slack': teams[0].slack,
    }


def test_core_teams_list(api_client, django_assert_max_num_queries):
    teams = CoreTeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(3):
        r = api_client.get(reverse('coreteam-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
        'team_members_meta': [{
            'team': team_member.team_id,
            'user': team_member.user_id,
            'is_lead': team_member.is_lead,
            'pay_per_day': team_member.pay_per_day,
            'job_title': team_member.job_title,
            'created_date': serializers.DateTimeField().to_representation(team_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(team_member.modified_date),
        } for team_member in teams[0].team_members.order_by('created_date').all()],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'slack': teams[0].slack,
        'responsibilities': teams[0].responsibilities,
    }


def test_project_teams_list(api_client, django_assert_max_num_queries):
    teams = ProjectTeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(3):
        r = api_client.get(reverse('projectteam-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
        'team_members_meta': [{
            'team': team_member.team_id,
            'user': team_member.user_id,
            'is_lead': team_member.is_lead,
            'pay_per_day': team_member.pay_per_day,
            'job_title': team_member.job_title,
            'created_date': serializers.DateTimeField().to_representation(team_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(team_member.modified_date),
        } for team_member in teams[0].team_members.order_by('created_date').all()],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'slack': teams[0].slack,
        'external_url': teams[0].external_url,
        'is_active': teams[0].is_active,
    }


def test_teams_members_empty_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('team-list'), data={
            'title': 'Star team',
            'about': 'About Star team',
            'github': 'https://github.com/thenewboston-developers'
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'team_members_meta': [],
        'title': 'Star team',
        'about': 'About Star team',
        'github': 'https://github.com/thenewboston-developers',
        'slack': r.data['slack'],
    }
    assert Team.objects.get(pk=r.data['pk']).title == 'Star team'


def test_teams_post(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)

    users = UserFactory.create_batch(5)

    with freeze_time() as frozen_time, django_assert_max_num_queries(6):
        r = api_client.post(reverse('team-list'), data={
            'title': 'Star team',
            'about': 'About Star team',
            'team_members_meta': [
                {
                    'user': users[1].pk,
                    'is_lead': True,
                    'pay_per_day': 19001,
                    'job_title': 'Back-End Developer'
                },
                {
                    'user': users[3].pk,
                    'is_lead': False,
                    'pay_per_day': 9001,
                    'job_title': 'Front-End Developer'
                }
            ],
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'team_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[1].pk,
                'team': ANY,
                'is_lead': True,
                'pay_per_day': 19001,
                'job_title': 'Back-End Developer'
            },
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[3].pk,
                'team': ANY,
                'is_lead': False,
                'pay_per_day': 9001,
                'job_title': 'Front-End Developer'
            }
        ],
        'title': 'Star team',
        'about': 'About Star team',
        'github': r.data['github'],
        'slack': r.data['slack'],
    }
    assert Team.objects.get(pk=r.data['pk']).title == 'Star team'


def test_core_teams_post(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)

    users = UserFactory.create_batch(5)

    with freeze_time() as frozen_time, django_assert_max_num_queries(7):
        r = api_client.post(reverse('coreteam-list'), data={
            'title': 'Star team',
            'about': 'About Star team',
            'responsibilities': 'Be awesome',
            'team_members_meta': [
                {
                    'user': users[1].pk,
                    'is_lead': True,
                    'pay_per_day': 19001,
                    'job_title': 'Back-End Developer'
                },
            ],
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'team_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[1].pk,
                'team': ANY,
                'is_lead': True,
                'pay_per_day': 19001,
                'job_title': 'Back-End Developer'
            },
        ],
        'title': 'Star team',
        'about': 'About Star team',
        'github': r.data['github'],
        'slack': r.data['slack'],
        'responsibilities': 'Be awesome',
    }
    assert CoreTeam.objects.get(pk=r.data['pk']).title == 'Star team'


def test_project_teams_post(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)

    users = UserFactory.create_batch(5)

    with freeze_time() as frozen_time, django_assert_max_num_queries(7):
        r = api_client.post(reverse('projectteam-list'), data={
            'title': 'Ether Team',
            'about': 'About Ether team',
            'external_url': 'https://github.com/google',
            'team_members_meta': [
                {
                    'user': users[1].pk,
                    'is_lead': True,
                    'pay_per_day': 19001,
                    'job_title': 'Go Developer'
                },
            ],
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'team_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[1].pk,
                'team': ANY,
                'is_lead': True,
                'pay_per_day': 19001,
                'job_title': 'Go Developer'
            },
        ],
        'title': 'Ether Team',
        'about': 'About Ether team',
        'github': r.data['github'],
        'slack': r.data['slack'],
        'external_url': 'https://github.com/google',
        'is_active': True
    }
    assert ProjectTeam.objects.get(pk=r.data['pk']).title == 'Ether Team'


def test_teams_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    user = UserFactory()
    team = TeamFactory(team_members=2)

    old_team_member = team.team_members.all()[1]

    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse('team-detail', (team.pk,)),
            data={
                'title': 'Star team',
                'about': 'About Star team',
                'team_members_meta': [
                    {
                        'user': old_team_member.user_id,
                        'is_lead': True,
                        'pay_per_day': 19001,
                        'job_title': 'Back-End Developer'
                    },
                    {
                        'user': user.pk,
                        'is_lead': False,
                        'pay_per_day': 9001,
                        'job_title': 'Front-End Developer'
                    }
                ]
            },
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(team.pk),
        'created_date': serializers.DateTimeField().to_representation(team.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'team_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(old_team_member.created_date),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': old_team_member.user_id,
                'team': team.pk,
                'is_lead': True,
                'pay_per_day': 19001,
                'job_title': 'Back-End Developer'
            },
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': user.pk,
                'team': team.pk,
                'is_lead': False,
                'pay_per_day': 9001,
                'job_title': 'Front-End Developer'
            },
        ],
        'title': 'Star team',
        'about': 'About Star team',
        'github': team.github,
        'slack': team.slack,
    }

    assert Team.objects.get(pk=str(team.pk)).title == 'Star team'


def test_teams_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    team = TeamFactory(team_members=2)

    r = api_client.delete(reverse('team-detail', (team.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Team.objects.filter(pk=str(team.pk)).first() is None


def test_opening_anon_post(api_client):
    r = api_client.post(reverse('team-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_teams_anon_patch(api_client):
    team = TeamFactory()

    r = api_client.post(reverse('team-detail', (team.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_teams_anon_delete(api_client):
    team = TeamFactory()

    r = api_client.delete(reverse('team-detail', (team.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
