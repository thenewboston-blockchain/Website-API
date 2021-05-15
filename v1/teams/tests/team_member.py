from unittest.mock import ANY

from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.team import CoreMemberFactory, CoreTeamFactory, ProjectMemberFactory, ProjectTeamFactory, TeamFactory, TeamMemberFactory


def test_teams_members_list(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(52):
        r = api_client.get(reverse('teammember-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 50
    assert r.data['results'][0] == {
        'pk': ANY,
        'user_data': {
            'account_number': teams[0].team_members.all()[0].user.account_number,
            'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].user.created_date),
            'display_name': teams[0].team_members.all()[0].user.display_name,
            'github_username': teams[0].team_members.all()[0].user.github_username,
            'is_email_verified': teams[0].team_members.all()[0].user.is_email_verified,
            'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].user.modified_date),
            'pk': str(teams[0].team_members.all()[0].user.pk),
            'profile_image': teams[0].team_members.all()[0].user.profile_image,
            'discord_username': teams[0].team_members.all()[0].user.discord_username,
        },
        'team': teams[0].pk,
        'is_lead': teams[0].team_members.all()[0].is_lead,
        'job_title': teams[0].team_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].modified_date),
    }


def test_teams_members_filter(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = TeamFactory()
    TeamMemberFactory.create(team=team, user=staff_user)
    TeamMemberFactory.create(team=team)
    r = api_client.get(reverse('teammember-list') + f'?user={staff_user.pk}')
    assert len(r.data['results']) == 1


def test_core_members_list(api_client, django_assert_max_num_queries):
    teams = CoreTeamFactory.create_batch(10, core_members=5)

    with django_assert_max_num_queries(52):
        r = api_client.get(reverse('coremember-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 50
    assert r.data['results'][0] == {
        'pk': ANY,
        'user_data': {
            'account_number': teams[0].core_members.all()[0].user.account_number,
            'created_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].user.created_date),
            'display_name': teams[0].core_members.all()[0].user.display_name,
            'github_username': teams[0].core_members.all()[0].user.github_username,
            'is_email_verified': teams[0].core_members.all()[0].user.is_email_verified,
            'modified_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].user.modified_date),
            'pk': str(teams[0].core_members.all()[0].user.pk),
            'profile_image': teams[0].core_members.all()[0].user.profile_image,
            'discord_username': teams[0].core_members.all()[0].user.discord_username,
        },
        'team': teams[0].core_members.all()[0].team.pk,
        'core_team': teams[0].pk,
        'is_lead': teams[0].core_members.all()[0].is_lead,
        'hourly_rate': teams[0].core_members.all()[0].hourly_rate,
        'weekly_hourly_commitment': teams[0].core_members.all()[0].weekly_hourly_commitment,
        'job_title': teams[0].core_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].modified_date),
    }


def test_core_members_filter(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    core_team = CoreTeamFactory()
    CoreMemberFactory.create(core_team=core_team, user=staff_user)
    CoreMemberFactory.create(core_team=core_team)
    r = api_client.get(reverse('coremember-list') + f'?user={staff_user.pk}')
    assert len(r.data['results']) == 1


def test_project_members_list(api_client, django_assert_max_num_queries):
    teams = ProjectTeamFactory.create_batch(10, project_members=5)

    with django_assert_max_num_queries(52):
        r = api_client.get(reverse('projectmember-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 50
    assert r.data['results'][0] == {
        'pk': ANY,
        'user_data': {
            'account_number': teams[0].project_members.all()[0].user.account_number,
            'created_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].user.created_date),
            'display_name': teams[0].project_members.all()[0].user.display_name,
            'github_username': teams[0].project_members.all()[0].user.github_username,
            'is_email_verified': teams[0].project_members.all()[0].user.is_email_verified,
            'modified_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].user.modified_date),
            'pk': str(teams[0].project_members.all()[0].user.pk),
            'profile_image': teams[0].project_members.all()[0].user.profile_image,
            'discord_username': teams[0].project_members.all()[0].user.discord_username,
        },
        'team': teams[0].project_members.all()[0].team.pk,
        'project_team': teams[0].pk,
        'is_lead': teams[0].project_members.all()[0].is_lead,
        'job_title': teams[0].project_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].modified_date),
    }


def test_project_members_filter(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project_team = ProjectTeamFactory()
    ProjectMemberFactory.create(project_team=project_team, user=staff_user)
    ProjectMemberFactory.create(project_team=project_team)
    r = api_client.get(reverse('projectmember-list') + f'?user={staff_user.pk}')
    assert len(r.data['results']) == 1


def test_teams_members_list_filter(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(4):
        r = api_client.get(f'{reverse("teammember-list")}?user={teams[0].team_members.all()[0].user_id}')

    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()['results']) == 1
    assert r.json()['results'][0] == {
        'pk': ANY,
        'user_data': {
            'account_number': teams[0].team_members.all()[0].user.account_number,
            'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].user.created_date),
            'display_name': teams[0].team_members.all()[0].user.display_name,
            'github_username': teams[0].team_members.all()[0].user.github_username,
            'is_email_verified': teams[0].team_members.all()[0].user.is_email_verified,
            'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].user.modified_date),
            'pk': str(teams[0].team_members.all()[0].user.pk),
            'profile_image': teams[0].team_members.all()[0].user.profile_image,
            'discord_username': teams[0].team_members.all()[0].user.discord_username,
        },
        'team': str(teams[0].pk),
        'is_lead': teams[0].team_members.all()[0].is_lead,
        'job_title': teams[0].team_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].modified_date),
    }


def test_teams_members_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = TeamFactory()

    r = api_client.post(reverse('teammember-list'), data={
        'user': staff_user.pk,
        'team': team.pk,
        'is_lead': False,
        'job_title': 'User',
    }, format='json')

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_core_members_post(api_client, superuser):
    api_client.force_authenticate(superuser)
    team = CoreTeamFactory()
    r = api_client.post(reverse('coremember-list'), data={
        'user': superuser.pk,
        'core_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
        'hourly_rate': 50,
        'weekly_hourly_commitment': 30
    }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_project_members_post(api_client, superuser):
    api_client.force_authenticate(superuser)
    team = ProjectTeamFactory()

    r = api_client.post(reverse('projectmember-list'), data={
        'user': superuser.pk,
        'project_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
    }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_core_members_staff_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = CoreTeamFactory()

    r = api_client.post(reverse('coremember-list'), data={
        'user': staff_user.pk,
        'core_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
        'hourly_rate': 2800
    }, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_project_members_staff_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = ProjectTeamFactory()

    r = api_client.post(reverse('projectmember-list'), data={
        'user': staff_user.pk,
        'project_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
    }, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_teams_members_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    team_member = TeamMemberFactory()

    r = api_client.patch(
        reverse('teammember-detail', (team_member.pk,)),
        data={
            'is_lead': True,
            'job_title': 'anotherTitle',

        },
        format='json'
    )

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_core_members_staff_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    core_member = CoreMemberFactory()

    r = api_client.patch(
        reverse('coremember-detail', (core_member.pk,)),
        data={
            'is_lead': True,
            'job_title': 'anotherTitle',

        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_core_members_teamlead_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    core_member = CoreMemberFactory.create(user=staff_user, is_lead=True)

    r = api_client.patch(
        reverse('coremember-detail', (core_member.pk,)),
        data={
            'is_lead': False,
            'job_title': 'anotherTitle',

        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_project_members_staff_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project_member = ProjectMemberFactory()
    project_member.is_lead = True
    project_member.save()

    r = api_client.patch(
        reverse('projectmember-detail', (project_member.pk,)),
        data={
            'is_lead': True,
            'job_title': 'anotherTitle',

        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_project_members_teamlead_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project_member = ProjectMemberFactory.create(is_lead=True, user=staff_user)

    r = api_client.patch(
        reverse('projectmember-detail', (project_member.pk,)),
        data={
            'is_lead': False,
            'job_title': 'anotherTitle',

        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_teams_members_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    team_member = TeamMemberFactory()

    r = api_client.delete(reverse('teammember-detail', (team_member.pk,)))

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_core_members_delete(api_client, superuser):
    api_client.force_authenticate(superuser)

    core_member = CoreMemberFactory()

    r = api_client.delete(reverse('coremember-detail', (core_member.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_core_members_teamlead_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    core_member = CoreMemberFactory.create(is_lead=True)

    r = api_client.delete(reverse('coremember-detail', (core_member.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_project_members_delete(api_client, superuser):
    api_client.force_authenticate(superuser)

    project_member = ProjectMemberFactory()

    r = api_client.delete(reverse('projectmember-detail', (project_member.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_project_members_teamlead_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    project_member = ProjectMemberFactory.create(is_lead=True)

    r = api_client.delete(reverse('projectmember-detail', (project_member.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_teams_members_anon_post(api_client):
    r = api_client.post(reverse('teammember-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_teams_members_anon_patch(api_client):
    team_member = TeamMemberFactory()

    r = api_client.post(reverse('teammember-detail', (team_member.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_teams_members_anon_delete(api_client):
    team_member = TeamMemberFactory()

    r = api_client.delete(reverse('teammember-detail', (team_member.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
