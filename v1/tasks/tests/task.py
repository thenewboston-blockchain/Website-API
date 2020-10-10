# -*- coding: utf-8 -*-
from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories import TaskFactory
from ..models import Task
from ...teams.factories import ContributorFactory


def test_task_list(api_client, django_assert_max_num_queries):
    tasks = TaskFactory.create_batch(10)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('task-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(tasks[0].pk),
        'title': tasks[0].title,
        'contributor': tasks[0].contributor_id,
        'repository': tasks[0].repository,
        'completed_date': tasks[0].completed_date,
        'amount': tasks[0].amount,
        'created_date': serializers.DateTimeField().to_representation(tasks[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(tasks[0].modified_date),
    }


def test_task_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributor = ContributorFactory()

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('task-list'), data={
            'title': 'New task',
            'contributor': contributor.pk,
            'repository': 'https://github.com/thenewboston-developers/Website-API/',
            'amount': 9001
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'title': 'New task',
        'contributor': contributor.pk,
        'repository': 'https://github.com/thenewboston-developers/Website-API/',
        'amount': 9001,
        'completed_date': None,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }
    assert Task.objects.get(pk=r.data['pk']).title == 'New task'


def test_task_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    contributor = ContributorFactory()
    task = TaskFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('task-detail', (task.pk,)), data={
            'title': 'New task',
            'contributor': contributor.pk,
            'repository': 'https://github.com/thenewboston-developers/Website-API/',
            'amount': 9001,
            'completed_date': '2020-12-12T23:59:59Z',
        }, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(task.pk),
        'title': 'New task',
        'contributor': contributor.pk,
        'repository': 'https://github.com/thenewboston-developers/Website-API/',
        'amount': 9001,
        'completed_date': '2020-12-12T23:59:59Z',
        'created_date': serializers.DateTimeField().to_representation(task.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
    }

    assert Task.objects.get(pk=str(task.pk)).title == 'New task'


def test_task_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    task = TaskFactory()

    r = api_client.delete(reverse('task-detail', (task.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Task.objects.filter(pk=str(task.pk)).first() is None


def test_opening_anon_post(api_client):
    r = api_client.post(reverse('task-list'), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_task_anon_patch(api_client):
    task = TaskFactory()

    r = api_client.post(reverse('task-detail', (task.pk,)), data={'title': 'sometitle'}, format='json')

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_task_anon_delete(api_client):
    task = TaskFactory()

    r = api_client.delete(reverse('task-detail', (task.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN
