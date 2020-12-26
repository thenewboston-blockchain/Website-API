# -*- coding: utf-8 -*-
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.team import TeamFactory, TeamMemberFactory


def test_teams_members_list(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('teammember-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 50
    assert r.data[0] == {
        'user': teams[0].team_members.all()[0].user_id,
        'team': teams[0].pk,
        'is_lead': teams[0].team_members.all()[0].is_lead,
        'pay_per_day': teams[0].team_members.all()[0].pay_per_day,
        'job_title': teams[0].team_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[0].team_members.all()[0].modified_date),
    }


def test_teams_members_list_filter(api_client, django_assert_max_num_queries):
    teams = TeamFactory.create_batch(10, team_members=5)

    with django_assert_max_num_queries(3):
        r = api_client.get(f'{reverse("teammember-list")}?user={teams[1].team_members.all()[0].user_id}')

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 1
    assert r.data[0] == {
        'user': teams[1].team_members.all()[0].user_id,
        'team': teams[1].pk,
        'is_lead': teams[1].team_members.all()[0].is_lead,
        'pay_per_day': teams[1].team_members.all()[0].pay_per_day,
        'job_title': teams[1].team_members.all()[0].job_title,
        'created_date': serializers.DateTimeField().to_representation(teams[1].team_members.all()[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(teams[1].team_members.all()[0].modified_date),
    }


def test_teams_members_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = TeamFactory()

    r = api_client.post(reverse('teammember-list'), data={
        'user': staff_user.pk,
        'team': team.pk,
        'is_lead': False,
        'job_title': 'User',
        'pay_per_day': 100,
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
            'pay_per_day': 10101

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

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_teams_members_anon_patch(api_client):
    team_member = TeamMemberFactory()

    r = api_client.post(reverse('teammember-detail', (team_member.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_teams_members_anon_delete(api_client):
    team_member = TeamMemberFactory()

    r = api_client.delete(reverse('teammember-detail', (team_member.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
