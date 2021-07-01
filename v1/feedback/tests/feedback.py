from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.feedback import FeedbackFactory


@patch('rest_framework.throttling.AnonRateThrottle.get_rate', MagicMock(return_value=None))
def test_feedback_list(api_client, django_assert_max_num_queries):
    FeedbackFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('feedback-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


@patch('rest_framework.throttling.AnonRateThrottle.get_rate', MagicMock(return_value=None))
def test_feedback_post(api_client):
    r = api_client.post(
        reverse('feedback-list'),
        data={
            'name': 'Hanzo Hasashi',
            'email': 'scorpion@mk.com',
            'message': 'Protector of the earth realm',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_201_CREATED


def test_feedback_forbidden_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    feedback = FeedbackFactory.create()
    r = api_client.patch(
        reverse('feedback-detail', (feedback.pk,)),
        data={
            'message': 'Avenger of the Hasashi clan',
        },
        format='json'
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_feedback_anon_delete(api_client):
    feedback = FeedbackFactory()
    r = api_client.delete(reverse('feedback-detail', (feedback.pk,)))
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_feedback_superuser_patch(api_client, superuser):
    api_client.force_authenticate(superuser)
    feedback = FeedbackFactory.create()
    r = api_client.patch(
        reverse('feedback-detail', (feedback.pk,)),
        data={
            'message': 'Avenger of the Hasashi clan',
        },
        format='json'
    )
    assert r.status_code == status.HTTP_200_OK


def test_feedback_superuser_delete(api_client):
    feedback = FeedbackFactory()
    r = api_client.delete(reverse('feedback-detail', (feedback.pk,)))
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
