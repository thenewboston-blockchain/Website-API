# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories import ContributorFactory
from ..models import Contributor


def test_contributor_list(api_client, django_assert_max_num_queries):
    contributors = ContributorFactory.create_batch(10)

    with django_assert_max_num_queries(5):
        r = api_client.get(reverse('contributor-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(contributors[0].pk),
        'display_name': contributors[0].display_name,
        'github_username': contributors[0].github_username,
        'slack_username': contributors[0].slack_username,
        'created_date': serializers.DateTimeField().to_representation(contributors[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(contributors[0].modified_date),
    }


def test_contributor_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('contributor-list'), data={
            'display_name': 'Super Dev',
            'github_username': 'super_githuber',
            'slack_username': 'super_slacker',
        })

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'display_name': 'Super Dev',
        'github_username': 'super_githuber',
        'slack_username': 'super_slacker',
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Contributor.objects.get(pk=r.data['pk']).display_name == 'Super Dev'


def test_contributor_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributor = ContributorFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('contributor-detail', (contributor.pk,)), data={
            'display_name': 'Senior Super Dev',
            'github_username': 'senior_super_githuber',
            'slack_username': 'senior_super_slacker',
        })

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(contributor.pk),
        'display_name': 'Senior Super Dev',
        'github_username': 'senior_super_githuber',
        'slack_username': 'senior_super_slacker',
        'created_date': serializers.DateTimeField().to_representation(contributor.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Contributor.objects.get(pk=str(contributor.pk)).display_name == 'Senior Super Dev'


def test_contributor_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributor = ContributorFactory()

    r = api_client.delete(reverse('contributor-detail', (contributor.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Contributor.objects.filter(pk=str(contributor.pk)).first() is None


def test_contributor_anon_post(api_client):
    r = api_client.post(reverse('contributor-list'), data={'title': 'sometitle'})

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_contributor_anon_patch(api_client):
    contributor = ContributorFactory()

    r = api_client.post(reverse('contributor-detail', (contributor.pk,)), data={'display_name': 'display_name'})

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_contributor_anon_delete(api_client):
    contributor = ContributorFactory()

    r = api_client.delete(reverse('contributor-detail', (contributor.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
