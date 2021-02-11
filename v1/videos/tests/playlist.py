from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.video import PlaylistFactory
from ..models.playlist import Playlist


def test_playlists_list(api_client, django_assert_max_num_queries):
    PlaylistFactory.create_batch(10, videos=5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('playlist-list'))
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10


def test_empty_videolist_post(api_client):
    with freeze_time() as frozen_time:
        r = api_client.post(reverse('playlist-list'), data={
            'playlist_id': 'qcYthscy9ok',
            'title': 'Native tutorials',
            'description': 'Episode two of our Detroit series',
            'published_at': '2020-12-03T20:00:10Z',
            'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
            'language': 'en',
            'playlist_type': 'youtube',
            'author': 'UCI5Sn4UBWZG-jarsmyBzr3Q',
        }, format='json')

    assert r.status_code == status.HTTP_201_CREATED
    assert Playlist.objects.get(pk=r.data['uuid']).title == 'Native tutorials'
    assert r.data == {
        'uuid': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'playlist_id': 'qcYthscy9ok',
        'title': 'Native tutorials',
        'description': 'Episode two of our Detroit series',
        'published_at': '2020-12-03T20:00:10Z',
        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
        'language': 'en',
        'playlist_type': 'youtube',
        'author': 'UCI5Sn4UBWZG-jarsmyBzr3Q',
        'video_list': []
    }


def test_playlist_patch(api_client):
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
                        'duration': 350,
                        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
                        'language': 'en',
                        'video_type': 'youtube',
                        'author': 'UCI5Sn4UBWZG-jarsmyBzr3Q',
                        'category': ['10']
                    },
                ]
            },
        )

    assert r.status_code == status.HTTP_200_OK
    assert Playlist.objects.get(pk=str(playlist.pk)).title == 'New title'


def test_playlists_delete(api_client, staff_user):
    playlist = PlaylistFactory(videos=2)
    r = api_client.delete(reverse('playlist-detail', (playlist.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert Playlist.objects.filter(pk=str(playlist.pk)).first() is None
