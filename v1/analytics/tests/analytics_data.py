from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.analytics import AnalyticsDataFactory, AnalyticsFactory
from ..models.analytics import AnalyticsData


def test_analytics_data_list(api_client, django_assert_max_num_queries):
    AnalyticsDataFactory.create_batch(5)
    with django_assert_max_num_queries(35):
        r = api_client.get(reverse('analyticsdata-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_analytics_data_filter_by_analytics(api_client, django_assert_max_num_queries):
    AnalyticsDataFactory.create_batch(3)
    analytics = AnalyticsFactory()
    AnalyticsDataFactory.create_batch(2, analytics=analytics)
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('analyticsdata-list') + f'?analytics={analytics.pk}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_analytics_data_filter_by_invalid_date(api_client, django_assert_max_num_queries):
    analytics = AnalyticsFactory()
    AnalyticsDataFactory.create_batch(2, analytics=analytics)
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('analyticsdata-list') + '?from=2021/07/03')
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Invalid date format, date must be in "YYYY-MM-DD' in r.data['detail']


def test_analytics_data_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics = AnalyticsFactory()
    AnalyticsDataFactory.create()

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('analyticsdata-list'), data={
            'analytics': analytics.pk,
            'date': '2021-07-13T20:00:10Z',
            'value': 300
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert AnalyticsData.objects.get(pk=r.data['pk']).value == 300
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'date': '2021-07-13T20:00:10Z',
        'value': 300,
        'analytics': analytics.pk
    }


def test_analytics_data_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics_data = AnalyticsDataFactory()

    with freeze_time():
        r = api_client.patch(
            reverse('analyticsdata-detail', (analytics_data.pk,)),
            data={
                'value': 430,
            },
        )

    assert r.status_code == status.HTTP_200_OK
    assert AnalyticsData.objects.get(pk=str(analytics_data.pk)).value == 430


def test_analytics_data_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    data = AnalyticsDataFactory()
    r = api_client.delete(reverse('analyticsdata-detail', (data.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert AnalyticsData.objects.filter(pk=str(data.pk)).first() is None


def test_analytics_data_anon_post(api_client):
    r = api_client.post(reverse('analyticsdata-list'), data={'value': 100}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
