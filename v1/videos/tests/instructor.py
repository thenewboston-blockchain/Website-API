from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.video import InstructorFactory


def test_instructors_list(api_client, django_assert_max_num_queries):
    InstructorFactory.create_batch(5)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('instructor-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_instructor_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    r = api_client.post(reverse('instructor-list'), data={'name': 'Jane Dough',
                                                          'youtube_url': 'https://www.youtube.com/channel/UC8wk1I01SpvpmGQuhQykGiA',
                                                          'vimeo_url': 'https://www.youtube.com/channel/UC8wk1I01SpvpmGQuhQykGiA'
                                                          }, format='json')

    assert r.status_code == status.HTTP_201_CREATED


def test_instructor_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    instructor = InstructorFactory()

    r = api_client.patch(
        reverse('instructor-detail', (instructor.pk,)),
        data={
            'name': 'Jane Doe',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK


def test_instructor_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    instructor = InstructorFactory()

    r = api_client.delete(reverse('instructor-detail', (instructor.pk,)))
    assert r.status_code == status.HTTP_204_NO_CONTENT


def test_instructor_anon_post(api_client):
    r = api_client.post(reverse('instructor-list'), data={'name': 'instructor'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_instructor_anon_patch(api_client):
    instructor = InstructorFactory()

    r = api_client.post(reverse('instructor-detail', (instructor.pk,)), data={'name': 'instructor'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_instructor_anon_delete(api_client):
    instructor = InstructorFactory()

    r = api_client.delete(reverse('instructor-detail', (instructor.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
