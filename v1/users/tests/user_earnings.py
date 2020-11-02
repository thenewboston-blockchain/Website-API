# -*- coding: utf-8 -*-
import random

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.constants.network import MAX_POINT_VALUE

from ..factories.user import UserFactory
from ..models.user_earnings import UserEarnings


@pytest.fixture
def repositories():
    yield (
        'Bank',
        'Validator',
        'Website-API',
    )


@pytest.fixture
def users(repositories):
    yield UserFactory.create_batch(10, repositories=repositories)


def test_user_list(api_client, django_assert_max_num_queries, users, repositories):
    with django_assert_max_num_queries(5):
        result = api_client.get(reverse('userearnings-list'))

    assert result.status_code == HTTP_200_OK
    assert len(result.data) == len(users) * len(repositories) * len(UserEarnings.TimePeriod.values)


def test_user_list_filtered(api_client, django_assert_max_num_queries, users, repositories):
    repository = random.choice(repositories)
    time_period = random.choice(UserEarnings.TimePeriod.values)

    with django_assert_max_num_queries(5):
        result = api_client.get(
            reverse('userearnings-list') + f'?repository={repository}&time_period={time_period}'
        )

    assert result.status_code == HTTP_200_OK
    assert len(result.data) == len(users)

    previous_amount = MAX_POINT_VALUE
    for user_earnings in result.data:
        assert user_earnings['user']
        assert user_earnings['repository'] == repository
        assert user_earnings['time_period'] == time_period
        assert user_earnings['total_amount'] <= previous_amount
        previous_amount = user_earnings['total_amount']
