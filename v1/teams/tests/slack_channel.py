from unittest.mock import ANY

from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.reverse import reverse

from ..factories.team import SlackChannelFactory
from ..models.slack_channel import SlackChannel


def test_slack_channels_list(api_client, django_assert_max_num_queries):
    slack_channels = SlackChannelFactory.create_batch(10)
    with django_assert_max_num_queries(2):
        r = api_client.get(reverse('slackchannel-list'), {'limit': 0})

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 10
    assert r.data[0] == {
        'pk': str(slack_channels[0].pk),
        'created_date': serializers.DateTimeField().to_representation(slack_channels[0].created_date),
        'modified_date': serializers.DateTimeField().to_representation(slack_channels[0].modified_date),
        'name': slack_channels[0].name,
        'team': slack_channels[0].team.pk
    }


def test_slack_channel_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    with freeze_time() as frozen_time:
        r = api_client.post(
            reverse('slackchannel-list'),
            data={
                'name': 'smart contracts',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == {
        'pk': ANY,
        'created_date': serializers.DateTimeField().to_representation(frozen_time()),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'name': 'smart contracts',
        'team': ANY
    }
    assert SlackChannel.objects.get(pk=r.data['pk']).name == 'smart contracts'


def test_slack_channel_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    slack_channel = SlackChannelFactory()
    with freeze_time() as frozen_time:
        r = api_client.patch(
            reverse('slackchannel-detail', (slack_channel.pk,)),
            data={
                'name': 'exchanges',
            },
            format='json'
        )

    assert r.status_code == status.HTTP_200_OK
    assert r.data == {
        'pk': str(slack_channel.pk),
        'created_date': serializers.DateTimeField().to_representation(slack_channel.created_date),
        'modified_date': serializers.DateTimeField().to_representation(frozen_time()),
        'name': 'exchanges',
        'team': slack_channel.team.pk
    }
    assert SlackChannel.objects.get(pk=str(slack_channel.pk)).name == 'exchanges'


def test_slack_channel_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    slack_channel = SlackChannelFactory()
    r = api_client.delete(reverse('slackchannel-detail', (slack_channel.pk,)))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert r.data is None
    assert SlackChannel.objects.filter(pk=str(slack_channel.pk)).first() is None


def test_slack_channel_anon_post(api_client):
    r = api_client.post(reverse('slackchannel-list'), data={'name': 'somename'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_slack_channel_anon_patch(api_client):
    slack_channel = SlackChannelFactory()
    r = api_client.post(reverse('slackchannel-detail', (slack_channel.pk,)), data={'name': 'somename'}, format='json')

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_slack_channel_anon_delete(api_client):
    slack_channel = SlackChannelFactory()
    r = api_client.delete(reverse('slackchannel-detail', (slack_channel.pk,)))

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
