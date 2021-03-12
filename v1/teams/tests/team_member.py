from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.team import CoreTeamFactory, ProjectTeamFactory, TeamFactory, TeamMemberFactory


def test_teams_members_list(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('teammember-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 50
    assert r.data[0] == {
        'user': teams[0].team_members.all()[0].user_id,
        'team': teams[0].pk,
        'is_lead': teams[0].team_members.all()[0].is_lead,
        'job_title': teams[0].team_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].modified_date),
    }


def test_core_members_list(api_client, django_assert_max_num_queries):
    teams = CoreTeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('coremember-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 50
    assert r.data[0] == {
        'user': teams[0].core_members.all()[0].user_id,
        'team': teams[0].core_members.all()[0].team.pk,
        'core_team': teams[0].pk,
        'is_lead': teams[0].core_members.all()[0].is_lead,
        'pay_per_day': teams[0].core_members.all()[0].pay_per_day,
        'job_title': teams[0].core_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].core_members.all()[0].modified_date),
    }


def test_project_members_list(api_client, django_assert_max_num_queries):
    teams = ProjectTeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('projectmember-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 50
    assert r.data[0] == {
        'user': teams[0].project_members.all()[0].user_id,
        'team': teams[0].project_members.all()[0].team.pk,
        'project_team': teams[0].pk,
        'is_lead': teams[0].project_members.all()[0].is_lead,
        'job_title': teams[0].project_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].project_members.all()[0].modified_date),
    }


def test_teams_members_list_filter(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(4):
        r = api_client.get(f'{reverse("teammember-list")}?user={teams[0].team_members.all()[0].user_id}')

    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()['results']) == 1
    assert r.json()['results'][0] == {
        'user': str(teams[0].team_members.all()[0].user_id),
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


def test_core_members_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = CoreTeamFactory()

    r = api_client.post(reverse('coremember-list'), data={
        'user': staff_user.pk,
        'core_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
        'pay_per_day': 2800
    }, format='json')

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_project_members_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = ProjectTeamFactory()

    r = api_client.post(reverse('projectmember-list'), data={
        'user': staff_user.pk,
        'project_team': team.pk,
        'is_lead': False,
        'job_title': 'User',
    }, format='json')

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


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


def test_teams_members_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    team_member = TeamMemberFactory()

    r = api_client.delete(reverse('teammember-detail', (team_member.pk,)))

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


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
