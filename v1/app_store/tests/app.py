from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.app import AppFactory


def test_apps_list(api_client, django_assert_max_num_queries):
    AppFactory.create_batch(5)
    with django_assert_max_num_queries(35):
        r = api_client.get(reverse('app-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4
