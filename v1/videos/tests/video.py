from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.video import PlaylistFactory, VideoFactory


def test_playlists_videos_list(api_client, django_assert_max_num_queries):
    PlaylistFactory.create_batch(10, videos=5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('video-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 50


def test_video_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    playlist = PlaylistFactory()

    r = api_client.post(reverse('video-list'), data={
        'playlist': playlist.pk,
        'video_id': 'qcYthscy9ok',
        'title': 'Fight Groove',
        'description': 'Episode two of our Detroit series',
        'published_at': '2020-12-03T20:00:10Z',
        'duration': 350,
        'thumbnail': 'https://i.ytimg.com/vi/qcYthscy9ok/default.jpg',
        'language': 'en',
        'video_type': 'youtube',
        'author': 'UCI5Sn4UBWZG-jarsmyBzr3Q',
        'category': ['10']
    }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_video_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    video = VideoFactory()

    r = api_client.patch(
        reverse('video-detail', (video.pk,)),
        data={
            'title': 'New title',
            'description': 'Episode that follows',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_video_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    video = VideoFactory()

    r = api_client.delete(reverse('video-detail', (video.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_video_anon_post(api_client):
    r = api_client.post(reverse('video-list'), data={'title': 'Video title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_video_anon_patch(api_client):
    video = VideoFactory()

    r = api_client.post(reverse('video-detail', (video.pk,)), data={'title': 'Video title'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_video_anon_delete(api_client):
    video = VideoFactory()

    r = api_client.delete(reverse('video-detail', (video.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
