from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.analytics import AnalyticsCategoryFactory, AnalyticsFactory
from ..models.analytics import AnalyticsCategory


def test_analytics_categories_list(api_client, django_assert_max_num_queries):
    AnalyticsCategoryFactory.create_batch(5)
    with django_assert_max_num_queries(35):
        r = api_client.get(reverse('analyticscategory-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_analytics_category_filter_by_key(api_client, django_assert_max_num_queries):
    AnalyticsCategoryFactory.create_batch(3)
    AnalyticsCategoryFactory.create_batch(2, key='economy')
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('analyticscategory-list') + '?key=economy')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_analytics_category_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics = AnalyticsFactory.create()

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('analyticscategory-list'), data={
            'title': 'Facebook',
            'key': 'facebook',
            'analytics': [analytics.pk]
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert AnalyticsCategory.objects.get(pk=r.data['pk']).title == 'Facebook'
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'Facebook',
        'key': 'facebook',
        'analytics': [analytics.pk]
    }


def test_analytics_category_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    analytics_category = AnalyticsCategoryFactory()

    with freeze_time():
        r = api_client.patch(
            reverse('analyticscategory-detail', (analytics_category.pk,)),
            data={
                'title': 'New title',
                'analytics': []
            },
        )

    assert r.status_code == status.HTTP_200_OK
    assert AnalyticsCategory.objects.get(pk=str(analytics_category.pk)).title == 'New title'


def test_analytics_category_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = AnalyticsCategoryFactory()
    r = api_client.delete(reverse('analyticscategory-detail', (category.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert AnalyticsCategory.objects.filter(pk=str(category.pk)).first() is None


def test_analytics_category_anon_post(api_client):
    r = api_client.post(reverse('analyticscategory-list'), data={'title': 'title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
