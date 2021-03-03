from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.repositories import RepositoryFactory
from ..models.repository import Repository


def test_repositories_list(api_client, django_assert_max_num_queries):
    repositories = RepositoryFactory.create_batch(10)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('repository-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(repositories[0].pk),
        'created_date': serializers.DateTimeField().to_representation(repositories[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(repositories[0].modified_date),
        'display_name': repositories[0].display_name,
        'url': repositories[0].url,
        'team': repositories[0].team.pk
    }


def test_repositories_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('repository-list'),
            data={
                'display_name': 'SuperRepo',
                'url': 'https://github.com/repo/super/'
            },
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'display_name': 'SuperRepo',
        'url': 'https://github.com/repo/super/',
        'team': ANY
    }

    assert Repository.objects.get(pk=r.data['pk']).display_name == 'SuperRepo'


def test_repositories_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    repository = RepositoryFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse('repository-detail', (repository.pk,)),
            data={
                'display_name': 'MyLittleRepo',
                'url': 'https://github.com/google/search/',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(repository.pk),
        'created_date': serializers.DateTimeField().to_representation(repository.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'display_name': 'MyLittleRepo',
        'url': 'https://github.com/google/search/',
        'team': repository.team.pk
    }

    assert Repository.objects.get(pk=str(repository.pk)).display_name == 'MyLittleRepo'


def test_repositories_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    repository = RepositoryFactory()

    r = api_client.delete(reverse('repository-detail', (repository.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Repository.objects.filter(pk=str(repository.pk)).first() is None


def test_repositories_anon_post(api_client):
    r = api_client.post(reverse('repository-list'), data={'display_name': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_repositories_anon_patch(api_client):
    repository = RepositoryFactory()

    r = api_client.post(reverse('repository-detail', (repository.pk,)), data={'display_name': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_repositories_anon_delete(api_client):
    repository = RepositoryFactory()

    r = api_client.delete(reverse('repository-detail', (repository.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
