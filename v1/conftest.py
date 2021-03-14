import pytest
from django.conf import settings
from pytest_django.migrations import DisableMigrations
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    """Auto use fixture to init DB"""
    pass


@pytest.fixture(scope='session', autouse=True)
def migrations_disabled():
    """Auto use fixture to path disable migration when all tests are executed"""
    settings.MIGRATION_MODULES = DisableMigrations()
    yield None


@pytest.fixture()
def api_client():
    """DRF ApiClient test client fixture"""
    return APIClient()


@pytest.fixture()
def staff_user(django_user_model):
    """Creates staff user"""
    UserModel = django_user_model
    email = 'staff@example.com'

    try:
        user = UserModel._default_manager.get(email=email)
    except UserModel.DoesNotExist:
        extra_fields = {
            'is_staff': True
        }
        user = UserModel._default_manager.create_user(
            email, 'password', **extra_fields
        )
    return user


@pytest.fixture()
def superuser(django_user_model):
    """Creates superuser"""
    UserModel = django_user_model
    email = 'super@example.com'

    try:
        user = UserModel._default_manager.get(email=email)
    except UserModel.DoesNotExist:
        extra_fields = {
            'is_superuser': True
        }
        user = UserModel._default_manager.create_user(
            email, 'password', **extra_fields
        )
    return user
