from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.analytics import AnalyticsDataFactory, AnalyticsFactory
from ..models.analytics import Analytics


def test_analytics_list(api_client, django_assert_max_num_queries):
    AnalyticsFactory.create_batch(5)
    with django_assert_max_num_queries(35):
        r = api_client.get(reverse('analytics-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_analytics_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('analytics-list'), data={
            'title': 'Facebook likes',
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert Analytics.objects.get(pk=r.data['pk']).title == 'Facebook likes'
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'Facebook likes',
        'data': []
    }


def test_analytics_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics = AnalyticsFactory()
    data = AnalyticsDataFactory()

    with freeze_time():
        r = api_client.patch(
            reverse('analytics-detail', (analytics.pk,)),
            data={
                'title': 'Facebook followers',
                'data': [data.pk]
            },
        )

    assert r.status_code == status.HTTP_200_OK
    assert Analytics.objects.get(pk=str(analytics.pk)).title == 'Facebook followers'


def test_analytics_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics = AnalyticsFactory()
    r = api_client.delete(reverse('analytics-detail', (analytics.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert Analytics.objects.filter(pk=str(analytics.pk)).first() is None


def test_analytics_anon_post(api_client):
    r = api_client.post(reverse('analytics-list'), data={'title': 'title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
