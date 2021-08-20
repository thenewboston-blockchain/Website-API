from rest_framework import status
from rest_framework.reverse import reverse

from ..factories.trusted_bank import TrustedBankFactory


def test_trusted_banks_list(api_client, django_assert_max_num_queries):
    TrustedBankFactory.create_batch(5)
    with django_assert_max_num_queries(7):
        r = api_client.get(reverse('trustedbank-list'), {'limit': 0})
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == 5


def test_trusted_bank_retrieve(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    bank = TrustedBankFactory()
    r = api_client.get(reverse('trustedbank-detail', (bank.pk,)))
    assert r.status_code == status.HTTP_200_OK


def test_trusted_bank_post(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    r = api_client.post(reverse('trustedbank-list'),
                        data={
                            'ip_address': '0.0.0.0',
                            'protocol': 'https',
                            'port': '80',
    }, format='json')
    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_trusted_bank_patch(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    bank = TrustedBankFactory()
    r = api_client.patch(
        reverse('trustedbank-detail', (bank.pk,)),
        data={
            'port': '3000',
        },
        format='json'
    )

    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_trusted_bank_delete(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    bank = TrustedBankFactory()
    r = api_client.delete(reverse('trustedbank-detail', (bank.pk,)))
    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
