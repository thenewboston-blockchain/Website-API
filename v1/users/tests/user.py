# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.user import UserFactory
from ..models import User


def test_user_list(api_client, django_assert_max_num_queries, staff_user):
    api_client.force_authenticate(staff_user)
    users = UserFactory.create_batch(10)

    with django_assert_max_num_queries(5):
        r = api_client.get(reverse('user-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(users[0].pk),
        'created_date': serializers.DateTimeField().to_representation(users[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(users[0].modified_date),
        'account_number': users[0].account_number,
        'display_name': users[0].display_name,
        'github_username': users[0].github_username,
        'profile_image': '',
        'slack_username': users[0].slack_username,
    }


def test_user_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('user-list'),
            data={
                'account_number': '4ed6c42c98a9f9b521f434df41e7de87a1543940121c895f3fb383bb8585d3ec',
                'display_name': 'Super Dev',
                'github_username': 'super_githuber',
                'slack_username': 'super_slacker',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'account_number': '4ed6c42c98a9f9b521f434df41e7de87a1543940121c895f3fb383bb8585d3ec',
        'display_name': 'Super Dev',
        'github_username': 'super_githuber',
        'profile_image': '',
        'slack_username': 'super_slacker',
    }

    assert User.objects.get(pk=r.data['pk']).display_name == 'Super Dev'


def test_user_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    user = UserFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('user-detail', (user.pk,)), data={
            'display_name': 'Senior Super Dev',
            'github_username': 'senior_super_githuber',
            'slack_username': 'senior_super_slacker',
        }, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(user.pk),
        'created_date': serializers.DateTimeField().to_representation(user.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'account_number': user.account_number,
        'display_name': 'Senior Super Dev',
        'github_username': 'senior_super_githuber',
        'profile_image': '',
        'slack_username': 'senior_super_slacker',
    }

    assert User.objects.get(pk=str(user.pk)).display_name == 'Senior Super Dev'


def test_user_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    user = UserFactory()

    r = api_client.delete(reverse('user-detail', (user.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert User.objects.filter(pk=str(user.pk)).first() is None


def test_user_anon_post(api_client):
    r = api_client.post(reverse('user-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_user_anon_patch(api_client):
    user = UserFactory()

    r = api_client.post(
        reverse('user-detail', (user.pk,)),
        data={'display_name': 'display_name'},
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_user_anon_delete(api_client):
    user = UserFactory()

    r = api_client.delete(reverse('user-detail', (user.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
