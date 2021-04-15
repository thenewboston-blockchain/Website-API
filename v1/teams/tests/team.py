from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from v1.users.factories.user import UserFactory
from ..factories.team import ProjectMemberFactory, CoreMemberFactory, CoreTeamFactory, ProjectTeamFactory, TeamFactory
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
            'pk': str(team_member.pk),
            'team': team_member.team_id,
            'user': team_member.user_id,
            'is_lead': team_member.is_lead,
            'job_title': team_member.job_title,
            'created_date': serializers.DateTimeField().to_representation(team_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(team_member.modified_date),
        } for team_member in teams[0].team_members.order_by('created_date').all()],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'discord': teams[0].discord,
    }


def test_core_teams_list(api_client, django_assert_max_num_queries):
    teams = CoreTeamFactory.create_batch(2, core_members=5)
    with django_assert_max_num_queries(13):
        r = api_client.get(reverse('coreteam-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 2
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
        'core_members_meta': [{
            'pk': str(core_member.pk),
            'team': core_member.team_id,
            'core_team': core_member.core_team_id,
            'user': core_member.user_id,
            'is_lead': core_member.is_lead,
            'job_title': core_member.job_title,
            'hourly_rate': core_member.hourly_rate,
            'weekly_hourly_commitment': core_member.weekly_hourly_commitment,
            'created_date': serializers.DateTimeField().to_representation(core_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(core_member.modified_date),
        } for core_member in teams[0].core_members.order_by('created_date').all()],
        'team_members_meta': [],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'discord': teams[0].discord,
        'responsibilities': teams[0].responsibilities,
    }


def test_project_teams_list(api_client, django_assert_max_num_queries):
    teams = ProjectTeamFactory.create_batch(2, project_members=5)

    with django_assert_max_num_queries(13):
        r = api_client.get(reverse('projectteam-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 2
    assert r.data[0] == {
        'pk': str(teams[0].pk),
        'created_date': serializers.DateTimeField().to_representation(teams[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].modified_date),
        'project_members_meta': [{
            'pk': str(project_member.pk),
            'team': project_member.team_id,
            'project_team': project_member.project_team_id,
            'user': project_member.user_id,
            'is_lead': project_member.is_lead,
            'job_title': project_member.job_title,
            'created_date': serializers.DateTimeField().to_representation(project_member.created_date),
            'modified_date': serializers.DateTimeField().to_representation(project_member.modified_date),
        } for project_member in teams[0].project_members.order_by('created_date').all()],
        'team_members_meta': [],
        'title': teams[0].title,
        'about': teams[0].about,
        'github': teams[0].github,
        'discord': teams[0].discord,
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
        'discord': r.data['discord'],
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
                    'job_title': 'Back-End Developer'
                },
                {
                    'user': users[3].pk,
                    'is_lead': False,
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
                'job_title': 'Back-End Developer',
                'pk': ANY,
            },
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[3].pk,
                'team': ANY,
                'is_lead': False,
                'job_title': 'Front-End Developer',
                'pk': ANY,
            }
        ],
        'title': 'Star team',
        'about': 'About Star team',
        'github': r.data['github'],
        'discord': r.data['discord'],
    }
    assert Team.objects.get(pk=r.data['pk']).title == 'Star team'


def test_core_teams_post(api_client, superuser, django_assert_max_num_queries):
    api_client.force_authenticate(superuser)

    users = UserFactory.create_batch(5)

    with freeze_time() as frozen_time, django_assert_max_num_queries(10):
        r = api_client.post(reverse('coreteam-list'), data={
            'title': 'Star team',
            'about': 'About Star team',
            'responsibilities': ['Be awesome'],
            'core_members_meta': [
                {
                    'user': users[1].pk,
                    'is_lead': True,
                    'job_title': 'Back-End Developer',
                    'hourly_rate': 2000,
                    'weekly_hourly_commitment': 50,
                },
            ],
        }, format='json')
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'core_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[1].pk,
                'team': ANY,
                'core_team': ANY,
                'is_lead': True,
                'job_title': 'Back-End Developer',
                'hourly_rate': 2000,
                'weekly_hourly_commitment': 50,
                'pk': ANY
            },
        ],
        'team_members_meta': [],
        'title': 'Star team',
        'about': 'About Star team',
        'github': r.data['github'],
        'discord': r.data['discord'],
        'responsibilities': ['Be awesome'],
    }
    assert CoreTeam.objects.get(pk=r.data['pk']).title == 'Star team'


def test_project_teams_post(api_client, superuser, django_assert_max_num_queries):
    api_client.force_authenticate(superuser)

    users = UserFactory.create_batch(5)

    with freeze_time() as frozen_time, django_assert_max_num_queries(10):
        r = api_client.post(reverse('projectteam-list'), data={
            'title': 'Ether Team',
            'about': 'About Ether team',
            'external_url': 'https://github.com/google',
            'project_members_meta': [
                {
                    'user': users[1].pk,
                    'is_lead': True,
                    'job_title': 'Go Developer'
                },
            ],
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'project_members_meta': [
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': users[1].pk,
                'team': ANY,
                'project_team': ANY,
                'is_lead': True,
                'job_title': 'Go Developer',
                'pk': ANY
            },
        ],
        'team_members_meta': [],
        'title': 'Ether Team',
        'about': 'About Ether team',
        'github': r.data['github'],
        'discord': r.data['discord'],
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
                        'hourly_rate': 19001,
                        'job_title': 'Back-End Developer'
                    },
                    {
                        'user': user.pk,
                        'is_lead': False,
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
                'job_title': 'Back-End Developer',
                'pk': ANY
            },
            {
                'created_date': serializers.DateTimeField().to_representation(frozen_time()),
                'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
                'user': user.pk,
                'team': team.pk,
                'is_lead': False,
                'job_title': 'Front-End Developer',
                'pk': ANY
            },
        ],
        'title': 'Star team',
        'about': 'About Star team',
        'github': team.github,
        'discord': team.discord,
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


def test_core_teams_staff_post(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    r = api_client.post(reverse('coreteam-list'), data={
        'title': 'Star team',
        'about': 'About Star team',
    }, format='json')
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_project_teams_staff_post(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    r = api_client.post(reverse('projectteam-list'), data={
        'title': 'Star team',
        'about': 'About Star team',
    }, format='json')
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_core_teams_staff_patch(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    core_team = CoreTeamFactory()
    r = api_client.post(reverse('coreteam-detail', (core_team.pk,)), data={'title': 'New Title'}, format='json')
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_core_teams_teamlead_patch(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    core_team = CoreTeamFactory()
    CoreMemberFactory.create(is_lead=True, user=staff_user, core_team=core_team)

    r = api_client.patch(reverse('coreteam-detail', (core_team.pk,)), data={'title': 'New Title'}, format='json')
    assert r.status_code == status.HTTP_200_OK


def test_project_teams_staff_patch(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    project_team = ProjectTeamFactory()
    r = api_client.post(reverse('projectteam-detail', (project_team.pk,)), data={'title': 'New Title'}, format='json')
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_project_teams_teamlead_patch(api_client, staff_user, django_assert_max_num_queries):
    api_client.force_authenticate(staff_user)
    project_team = ProjectTeamFactory()
    ProjectMemberFactory.create(is_lead=True, user=staff_user, project_team=project_team)

    r = api_client.patch(reverse('projectteam-detail', (project_team.pk,)), data={'title': 'New Title'}, format='json')
    assert r.status_code == status.HTTP_200_OK


def test_teams_anon_patch(api_client):
    team = TeamFactory()

    r = api_client.post(reverse('team-detail', (team.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_teams_anon_delete(api_client):
    team = TeamFactory()

    r = api_client.delete(reverse('team-detail', (team.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_core_team_anon_delete(api_client):
    core_team = CoreTeamFactory()

    r = api_client.delete(reverse('coreteam-detail', (core_team.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_project_team_superuser_delete(api_client, superuser):
    api_client.force_authenticate(superuser)
    project_team = ProjectTeamFactory()

    r = api_client.delete(reverse('projectteam-detail', (project_team.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
