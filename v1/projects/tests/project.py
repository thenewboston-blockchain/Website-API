from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.project import ProjectFactory
from ...teams.factories.team import ProjectMemberFactory


def test_projects_list(api_client, django_assert_max_num_queries):
    ProjectFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('project-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_project_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    lead = ProjectMemberFactory()
    r = api_client.post(reverse('project-list'), data={'title': 'TNBC Wallet',
                                                       'project_lead': lead.pk,
                                                       'description': 'Cold storage wallet',
                                                       'logo': 'https://avatars.githubusercontent.com/u/12706692?s=88&v=4',
                                                       'github_url': 'https://github.com/thenewboston-developers/Website-API',
                                                       'overview': 'Cold storage wallet',
                                                       'problem': 'Security for the store of wealth',
                                                       'target_market': 'Blockchain',
                                                       'benefits': 'Cold storage wallet',
                                                       'centered_around_tnb': 'yes',
                                                       'estimated_completion_date': '2021-05-03T20:00:10Z'
                                                       }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_project_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project = ProjectFactory()
    r = api_client.patch(
        reverse('project-detail', (project.pk,)),
        data={
            'description': 'Fintec',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_project_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    project = ProjectFactory()
    r = api_client.delete(reverse('project-detail', (project.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_project_anon_post(api_client):
    r = api_client.post(reverse('project-list'), data={'name': 'project'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_project_anon_patch(api_client):
    project = ProjectFactory()
    r = api_client.post(reverse('project-detail', (project.pk,)), data={'name': 'project'}, format='json')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_project_anon_delete(api_client):
    project = ProjectFactory()
    r = api_client.delete(reverse('project-detail', (project.pk,)))
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
