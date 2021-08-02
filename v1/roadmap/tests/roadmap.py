from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.roadmap import RoadmapFactory
from ...teams.factories.team import CoreTeamFactory


def test_roadmap_list(api_client, django_assert_max_num_queries):
    RoadmapFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('roadmap-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_roadmap_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    team = CoreTeamFactory()
    r = api_client.post(reverse('roadmap-list'),
                        data={
                            'team': team.pk,
                            'task_title': 'Launch beta',
                            'estimated_completion_date': '2021-09-30',
                            'is_complete': True
    }, format='json')
    assert r.status_code == status.HTTP_201_CREATED


def test_roadmap_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    roadmap = RoadmapFactory()
    r = api_client.patch(
        reverse('roadmap-detail', (roadmap.pk,)),
        data={
            'task_title': 'Plan beta',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_roadmap_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    roadmap = RoadmapFactory()
    r = api_client.delete(reverse('roadmap-detail', (roadmap.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_roadmap_anon_post(api_client):
    r = api_client.post(reverse('roadmap-list'), data={'task_title': 'roadmap'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_roadmap_anon_patch(api_client):
    roadmap = RoadmapFactory()
    r = api_client.post(reverse('roadmap-detail', (roadmap.pk,)), data={'task_title': 'roadmap'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_roadmap_anon_delete(api_client):
    roadmap = RoadmapFactory()
    r = api_client.delete(reverse('roadmap-detail', (roadmap.pk,)))
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
