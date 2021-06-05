from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.community import CommunityFactory


def test_community_analytics_list(api_client, django_assert_max_num_queries):
    CommunityFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('community-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5
