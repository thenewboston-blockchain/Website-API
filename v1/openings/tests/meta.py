# -*- coding: utf-8 -*-
from unittest.mock import ANY

import pytest
from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.responsibility import ResponsibilityFactory
from ..factories.skill import SkillFactory
from ..models.responsibility import Responsibility
from ..models.skill import Skill


@pytest.mark.parametrize('url_factory', [
    ('responsibility', ResponsibilityFactory),
    ('skill', SkillFactory)
])
def test_object_list(api_client, django_assert_max_num_queries, url_factory):
    url, factory = url_factory
    obj = factory.create_batch(5)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse(f'{url}-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
    assert r.data[0] == {
        'pk': str(obj[0].pk),
        'created_date': serializers.DateTimeField().to_representation(obj[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(obj[0].modified_date),
        'title': obj[0].title,
    }


@pytest.mark.parametrize('url_model', [
    ('responsibility', Responsibility),
    ('skill', Skill)
])
def test_object_staff_post(api_client, staff_user, url_model):
    url, model = url_model
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse(f'{url}-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'sometitle',
    }
    assert model.objects.get(pk=r.data['pk']).title == 'sometitle'


@pytest.mark.parametrize('url_factory_model', [
    ('responsibility', ResponsibilityFactory, Responsibility),
    ('skill', SkillFactory, Skill)
])
def test_object_staff_patch(api_client, staff_user, url_factory_model):
    url, factory, model = url_factory_model
    api_client.force_authenticate(staff_user)

    obj = factory()

    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse(f'{url}-detail', (obj.pk,)),
            data={'title': 'sometitle'},
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(obj.pk),
        'created_date': serializers.DateTimeField().to_representation(obj.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'sometitle',
    }
    assert model.objects.get(pk=r.data['pk']).title == 'sometitle'


@pytest.mark.parametrize('url_factory_model', [
    ('responsibility', ResponsibilityFactory, Responsibility),
    ('skill', SkillFactory, Skill)
])
def test_object_staff_delete(api_client, staff_user, url_factory_model):
    url, factory, model = url_factory_model
    api_client.force_authenticate(staff_user)

    obj = factory()

    r = api_client.delete(reverse(f'{url}-detail', (obj.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert model.objects.filter(pk=obj.pk).first() is None


@pytest.mark.parametrize('url', ['responsibility', 'skill'])
def test_object_anon_post(api_client, url):
    r = api_client.post(
        reverse(f'{url}-list'),
        data={'title': 'sometitle'},
        format='json'
    )

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('url_factory', [
    ('responsibility', ResponsibilityFactory),
    ('skill', SkillFactory)
])
def test_object_anon_patch(api_client, url_factory):
    url, factory = url_factory
    obj = factory()

    r = api_client.patch(
        reverse(f'{url}-detail', (obj.pk,)),
        data={'title': 'sometitle'},
        format='json'
    )

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('url_factory', [
    ('responsibility', ResponsibilityFactory),
    ('skill', SkillFactory)
])
def test_object_anon_delete(api_client, url_factory):
    url, factory = url_factory
    obj = factory()

    r = api_client.delete(reverse(f'{url}-detail', (obj.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
