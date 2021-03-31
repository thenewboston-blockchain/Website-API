from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.video import CategoryFactory


def test_categories_list(api_client, django_assert_max_num_queries):
    CategoryFactory.create_batch(5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('category-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_category_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    r = api_client.post(reverse('category-list'), data={'name': 'Science Fiction'
                                                        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_category_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = CategoryFactory()

    r = api_client.patch(
        reverse('category-detail', (category.pk,)),
        data={
            'name': 'New name',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_category_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = CategoryFactory()

    r = api_client.delete(reverse('category-detail', (category.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_category_anon_post(api_client):
    r = api_client.post(reverse('category-list'), data={'name': 'category'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_anon_patch(api_client):
    category = CategoryFactory()

    r = api_client.post(reverse('category-detail', (category.pk,)), data={'name': 'category'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_anon_delete(api_client):
    category = CategoryFactory()

    r = api_client.delete(reverse('category-detail', (category.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
