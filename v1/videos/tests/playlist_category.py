from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.video import PlaylistCategoryFactory


def test_playlist_categories_list(api_client, django_assert_max_num_queries):
    PlaylistCategoryFactory.create_batch(5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('playlistcategory-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_playlist_category_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    r = api_client.post(reverse('playlistcategory-list'), data={'name': 'Science Fiction'}, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_playlist_category_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = PlaylistCategoryFactory()

    r = api_client.patch(
        reverse('playlistcategory-detail', (category.pk,)),
        data={
            'name': 'New name',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_playlist_category_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = PlaylistCategoryFactory()

    r = api_client.delete(reverse('playlistcategory-detail', (category.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_playlist_category_anon_post(api_client):
    r = api_client.post(reverse('playlistcategory-list'), data={'name': 'category'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_playlist_category_anon_patch(api_client):
    category = PlaylistCategoryFactory()

    r = api_client.post(reverse('playlistcategory-detail', (category.pk,)), data={'name': 'category'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_playlist_category_anon_delete(api_client):
    category = PlaylistCategoryFactory()

    r = api_client.delete(reverse('playlistcategory-detail', (category.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
