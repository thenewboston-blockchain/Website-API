from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.project import MilestoneFactory, ProjectFactory


def test_milestone_list(api_client, django_assert_max_num_queries):
    MilestoneFactory.create_batch(5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('milestone-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_milestone_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project = ProjectFactory()
    r = api_client.post(reverse('milestone-list'), data={'project': project.pk, 'number': 1, 'description': 'Complete mockups'}, format='json')
    assert r.status_code == status.HTTP_201_CREATED


def test_milestone_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    milestone = MilestoneFactory()
    r = api_client.patch(
        reverse('milestone-detail', (milestone.pk,)),
        data={
            'description': 'Design architecture',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_milestone_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    milestone = MilestoneFactory()
    r = api_client.delete(reverse('milestone-detail', (milestone.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_milestone_anon_post(api_client):
    r = api_client.post(reverse('milestone-list'), data={'name': 'milestone'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_milestone_anon_patch(api_client):
    milestone = MilestoneFactory()
    r = api_client.post(reverse('milestone-detail', (milestone.pk,)), data={'description': 'milestone'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_milestone_anon_delete(api_client):
    milestone = MilestoneFactory()
    r = api_client.delete(reverse('milestone-detail', (milestone.pk,)))
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
