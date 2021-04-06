from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.video import CategoryFactory, PlaylistFactory, VideoFactory


def test_playlists_videos_list(api_client, django_assert_max_num_queries):
    PlaylistFactory.create_batch(5, videos=5)
    with django_assert_max_num_queries(28):
        r = api_client.get(reverse('video-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 25


def test_videos_filter_by_category(api_client, django_assert_max_num_queries):
    category = CategoryFactory.create()
    VideoFactory.create_batch(3)
    VideoFactory.create_batch(2, categories=[category.pk])
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('video-list') + f'?category={category.name}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 2


def test_videos_filter_by_playlist(api_client, django_assert_max_num_queries):
    playlist = PlaylistFactory.create()
    VideoFactory.create_batch(3)
    VideoFactory.create_batch(2, playlist=playlist)
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('video-list') + f'?playlist={str(playlist.uuid)}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 2


def test_videos_filter_by_category_and_playlist(api_client, django_assert_max_num_queries):
    category = CategoryFactory.create()
    playlist = PlaylistFactory.create()
    VideoFactory.create_batch(3)
    VideoFactory.create(playlist=playlist)
    VideoFactory.create(categories=[category.pk], playlist=playlist)
    with django_assert_max_num_queries(10):
        r = api_client.get(reverse('video-list') + f'?category={category.name}&playlist={str(playlist.uuid)}')
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data['results']) == 1


def test_video_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    category = CategoryFactory.create_batch(2)
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
        'categories': [category[0].pk]
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
