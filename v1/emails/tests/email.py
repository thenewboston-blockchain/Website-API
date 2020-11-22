# -*- coding: utf-8 -*-
from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.email import EmailFactory
from ..models.email import Email


def test_email_list(api_client, django_assert_max_num_queries):
    emails = EmailFactory.create_batch(10)

    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('email-list'))

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'email': emails[0].email,
        'subscribed': emails[0].subscribed,
        'created_at': serializers.DateTimeField().to_representation(emails[0].created_at),
        'modified_at': serializers.DateTimeField().to_representation(emails[0].modified_at)
    }


def test_email_post(api_client):
    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('email-list'),
            data={'email': 'user@example.com'},
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'email': 'user@example.com',
        'subscribed': True,
        'created_at': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_at': serializers.DateTimeField().to_representation(frozen_time()),
    }
    assert Email.objects.get(email=r.data['email']).email == 'user@example.com'


def test_email_patch(api_client):
    email = EmailFactory()

    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse('email-detail', (email.pk,)),
            data={'subscribed': False},
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'created_at': serializers.DateTimeField().to_representation(email.created_at),
        'modified_at': serializers.DateTimeField().to_representation(frozen_time()),
        'email': email.email,
        'subscribed': False
    }

    updated_email = Email.objects.get(pk=str(email.pk))
    assert updated_email.subscribed is False
    assert updated_email.email == email.email


def test_email_delete(api_client):
    email = EmailFactory()

    r = api_client.delete(reverse('email-detail', (email.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None

    assert Email.objects.filter(pk=str(email.pk)).first() is None


def test_email_blank(api_client):
    r = api_client.post(
        reverse('email-list'),
        data={'email': ''},
        format='json'
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {
        'email': [
            'This field may not be blank.'
        ]
    }


def test_email_anon_unique(api_client):
    email = EmailFactory()

    r = api_client.post(
        reverse('email-list'),
        data={'email': email.email},
        format='json'
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {
        'email': [
            'email with this email already exists.'
        ]
    }
