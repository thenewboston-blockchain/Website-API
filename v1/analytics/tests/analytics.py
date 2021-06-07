from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.community import CommunityFactory
from ..factories.economy import EconomyFactory
from ..factories.facebook import FacebookFactory
from ..factories.instagram import InstagramFactory
from ..factories.linkedin import LinkedInFactory
from ..factories.network import NetworkFactory
from ..factories.twitter import TwitterFactory


def test_community_analytics_list(api_client, django_assert_max_num_queries):
    CommunityFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('community-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_economy_analytics_list(api_client, django_assert_max_num_queries):
    EconomyFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('economy-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_network_analytics_list(api_client, django_assert_max_num_queries):
    NetworkFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('network-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_facebook_analytics_list(api_client, django_assert_max_num_queries):
    FacebookFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('facebook-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_instagram_analytics_list(api_client, django_assert_max_num_queries):
    InstagramFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('instagram-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_linkedin_analytics_list(api_client, django_assert_max_num_queries):
    LinkedInFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('linkedin-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_twitter_analytics_list(api_client, django_assert_max_num_queries):
    TwitterFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('twitter-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
