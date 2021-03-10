from unittest.mock import ANY, MagicMock, patch

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse


from ..factories.user import UserFactory
from ..models import User
from ...utils.verification import generate_token


def test_anon_delete(api_client):
    user = UserFactory()

    r = api_client.delete(reverse('user-detail', (user.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_anon_list(api_client, django_assert_max_num_queries):
    users = UserFactory.create_batch(10)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('user-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'account_number': users[0].account_number,
        'created_date': serializers.DateTimeField().to_representation(users[0].created_date),
        'display_name': users[0].display_name,
        'github_username': users[0].github_username,
        'is_email_verified': users[0].is_email_verified,
        'modified_date': serializers.DateTimeField().to_representation(users[0].modified_date),
        'pk': str(users[0].pk),
        'profile_image': '',
        'slack_username': users[0].slack_username,
    }


def test_anon_patch(api_client):
    user = UserFactory()

    r = api_client.patch(
        reverse('user-detail', (user.pk,)),
        data={
            'display_name': 'Bob'
        },
        format='json'
    )

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@patch('v1.users.views.user.send_account_email', MagicMock(return_value=None))
def test_anon_post(api_client):
    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('user-list'),
            data={
                'email': 'bucky@email.com',
                'password': 'Pswd43234!',
                'display_name': 'Bucky'
            },
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'account_number': '',
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'display_name': 'Bucky',
        'github_username': '',
        'is_email_verified': False,
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'pk': ANY,
        'profile_image': '',
        'slack_username': '',
    }
    assert User.objects.get(pk=r.data['pk']).display_name == 'Bucky'


@patch('v1.users.views.user.send_account_email', MagicMock(return_value=None))
def test_user_verification(api_client):
    api_client.post(
        reverse('user-list'),
        data={
            'email': 'bucky@email.com',
            'password': 'Pswd43234!',
            'display_name': 'Bucky'
        },
        format='json'
    )
    uid = urlsafe_base64_encode(force_bytes('bucky@email.com'))
    token = generate_token('bucky@email.com')
    r = api_client.get(reverse('user-list') + '/verify/{}/{}'.format(uid, token),
                       format='json'
                       )
    assert r.status_code == status.HTTP_200_OK
    is_token = 'access_token' in dict(r.data)['authentication']
    assert is_token


def test_invalid_token_verification(api_client):
    uid = urlsafe_base64_encode(force_bytes('bucky@email.com'))
    token = 'randomstring'
    r = api_client.get(reverse('user-list') + '/verify/{}/{}'.format(uid, token),
                       format='json'
                       )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data['message'] == 'Token is invalid'


@patch('v1.users.views.user.send_account_email', MagicMock(return_value=None))
def test_user_generate_new_link(api_client):
    api_client.post(
        reverse('user-list'),
        data={
            'email': 'test@thenewboston.com',
            'password': '@secret123',
            'display_name': 'Bucky'
        },
        format='json'
    )
    r = api_client.post(
        reverse('user-list') + '/new-link',
        data={
            'email': 'test@thenewboston.com',
            'req_type': 'verify'
        },
        format='json'
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'mesage': 'A new link has been sent to your email'
    }


def test_anon_post_common_password(api_client):
    r = api_client.post(
        reverse('user-list'),
        data={
            'email': 'bucky@email.com',
            'password': 'pass1234',
            'display_name': 'Bucky'
        },
        format='json'
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_other_user_delete(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    api_client.force_authenticate(user1)

    r = api_client.delete(reverse('user-detail', (user2.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_other_user_patch(api_client):
    user1 = UserFactory()
    user2 = UserFactory()
    api_client.force_authenticate(user1)

    r = api_client.patch(
        reverse('user-detail', (user2.pk,)),
        data={
            'display_name': 'Senior Super Dev',
            'github_username': 'senior_super_githuber',
            'slack_username': 'senior_super_slacker',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_other_user_post(api_client):
    user = UserFactory()
    api_client.force_authenticate(user)

    r = api_client.post(
        reverse('user-list'),
        data={
            'account_number': '4ed6c42c98a9f9b521f434df41e7de87a1543940121c895f3fb383bb8585d3ec',
            'display_name': 'Super Dev',
            'github_username': 'super_githuber',
            'slack_username': 'super_slacker',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_self_delete(api_client):
    user = UserFactory()
    api_client.force_authenticate(user)

    r = api_client.delete(reverse('user-detail', (user.pk,)))

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_self_patch(api_client):
    user = UserFactory()
    api_client.force_authenticate(user)

    with freeze_time() as frozen_time:
        r = api_client.patch(reverse('user-detail', (user.pk,)), data={
            'display_name': 'I am a Senior Super Dev',
            'github_username': 'senior_super_githuber',
            'slack_username': 'senior_super_slacker',
        }, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'account_number': user.account_number,
        'created_date': serializers.DateTimeField().to_representation(user.created_date),
        'display_name': 'I am a Senior Super Dev',
        'github_username': 'senior_super_githuber',
        'is_email_verified': False,
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'pk': str(user.pk),
        'profile_image': '',
        'slack_username': 'senior_super_slacker',
    }
    assert User.objects.get(pk=str(user.pk)).display_name == 'I am a Senior Super Dev'


def test_staff_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    user = UserFactory()

    r = api_client.delete(reverse('user-detail', (user.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert User.objects.filter(pk=str(user.pk)).first() is None


def test_staff_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    user = UserFactory()

    r = api_client.patch(
        reverse('user-detail', (user.pk,)),
        data={
            'display_name': 'Senior Super Dev',
            'github_username': 'senior_super_githuber',
            'slack_username': 'senior_super_slacker',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_staff_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)

    r = api_client.post(
        reverse('user-list'),
        data={
            'email': 'bucky@email.com',
            'password': 'Pswd43234!',
            'display_name': 'Bucky'
        },
        format='json'
    )

    assert r.status_code == status.HTTP_403_FORBIDDEN
