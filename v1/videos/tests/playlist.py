from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.video import InstructorFactory, PlaylistCategoryFactory, PlaylistFactory
from ..models.playlist import Playlist


def test_playlists_list(api_client, django_assert_max_num_queries):
    PlaylistFactory.create_batch(5, videos=5)
    with django_assert_max_num_queries(35):
        r = api_client.get(reverse('playlist-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_playlists_filter_by_category(api_client, django_assert_max_num_queries):
    category = PlaylistCategoryFactory.create()
    PlaylistFactory.create_batch(3)
    PlaylistFactory.create_batch(2, categories=[category.pk])
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('playlist-list') + f'?category={category.name}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_playlists_filter_by_instructor(api_client, django_assert_max_num_queries):
    instructor = InstructorFactory.create()
    PlaylistFactory.create_batch(3)
    PlaylistFactory.create_batch(2, instructor=instructor)
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('playlist-list') + f'?instructor={str(instructor.pk)}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 4


def test_playlists_filter_by_category_and_instructor(api_client, django_assert_max_num_queries):
    category = PlaylistCategoryFactory.create()
    instructor = InstructorFactory.create()
    PlaylistFactory.create_batch(3)
    PlaylistFactory.create(instructor=instructor, categories=[category.pk])
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('playlist-list') + f'?category={category.name}&instructor={str(instructor.pk)}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 1


def test_playlist_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = PlaylistCategoryFactory.create()
    instructor = InstructorFactory.create()

    with freeze_time() as frozen_time:
        r = api_client.post(reverse('playlist-list'), data={
            'title': 'Native tutorials',
            'description': 'Episode two of our Detroit series',
            'published_at': '2020-12-03T20:00:10Z',
            'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
            'categories': [category.pk],
            'playlist_type': 'youtube',
            'instructor': instructor.pk,
            'video_list': [{
                'video_id': 'qcYthscy9ok',
                'title': 'Fight Groove',
                'description': 'Episode two of our Detroit series',
                'published_at': '2020-12-03T20:00:10Z',
                'duration_seconds': 350,
                'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
                'position': 1,
            }]
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert Playlist.objects.get(pk=r.data['pk']).title == 'Native tutorials'
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'Native tutorials',
        'description': 'Episode two of our Detroit series',
        'published_at': '2020-12-03T20:00:10Z',
        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
        'categories': [category.pk],
        'playlist_type': 'youtube',
        'instructor': instructor.pk,
        'duration': 350,
        'video_list': [{
            'created_date': serializers.DateTimeField().to_representation(frozen_time()),
            'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
            'pk': ANY,
            'playlist': ANY,
            'video_id': 'qcYthscy9ok',
            'title': 'Fight Groove',
            'description': 'Episode two of our Detroit series',
            'published_at': '2020-12-03T20:00:10Z',
            'duration_seconds': 350,
            'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
            'position': 1,
        }]
    }


def test_empty_videolist_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = PlaylistCategoryFactory.create()
    instructor = InstructorFactory.create()
    with freeze_time() as frozen_time:
        r = api_client.post(reverse('playlist-list'), data={
            'title': 'Native tutorials',
            'description': 'Episode two of our Detroit series',
            'published_at': '2020-12-03T20:00:10Z',
            'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
            'playlist_type': 'youtube',
            'categories': [category.pk],
            'instructor': instructor.pk,
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert Playlist.objects.get(pk=r.data['pk']).title == 'Native tutorials'
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'title': 'Native tutorials',
        'description': 'Episode two of our Detroit series',
        'published_at': '2020-12-03T20:00:10Z',
        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
        'playlist_type': 'youtube',
        'categories': [category.pk],
        'instructor': instructor.pk,
        'video_list': [],
        'duration': 0,
    }


def test_invalid_playlist_datetime_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = PlaylistCategoryFactory.create()
    instructor = InstructorFactory.create()

    r = api_client.post(reverse('playlist-list'), data={
        'playlist_id': 'qcYthscy9ok',
        'title': 'Native tutorials',
        'published_at': '2020-12-03',
        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
        'playlist_type': 'youtube',
        'categories': [category.pk],
        'instructor': instructor.pk,
    }, format='json')
    assert 'Datetime has wrong format' in str(r.data['published_at'])
    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_playlist_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    playlist = PlaylistFactory(videos=2)

    with freeze_time():
        r = api_client.patch(
            reverse('playlist-detail', (playlist.pk,)),
            data={
                'title': 'New title',
                'description': 'Episode two',
                'video_list': [
                    {
                        'playlist': playlist.pk,
                        'video_id': 'qcYthscy9ok',
                        'title': 'Fight Groove',
                        'description': 'Episode two of our Detroit series',
                        'duration_seconds': 350,
                        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
                        'position': 2
                    },
                ]
            },
        )

    assert r.status_code == status.HTTP_200_OK
    assert Playlist.objects.get(pk=str(playlist.pk)).title == 'New title'


def test_playlists_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    playlist = PlaylistFactory(videos=2)
    r = api_client.delete(reverse('playlist-detail', (playlist.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert Playlist.objects.filter(pk=str(playlist.pk)).first() is None


def test_playlist_anon_post(api_client):
    r = api_client.post(reverse('playlist-list'), data={'title': 'new title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_playlist_anon_patch(api_client):
    playlist = PlaylistFactory()

    r = api_client.post(reverse('playlist-detail', (playlist.pk,)), data={'title': 'new title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_platlist_anon_delete(api_client):
    playlist = PlaylistFactory()

    r = api_client.delete(reverse('playlist-detail', (playlist.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
