# -*- coding: utf-8 -*-
from django.conf import settings
import pytest
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
def staff_user(django_user_model, django_username_field):
    """Creates staff user"""
    UserModel = django_user_model
    username_field = django_username_field
    username = 'staff@example.com' if username_field == 'email' else 'staff'

    try:
        user = UserModel._default_manager.get(**{username_field: username})
    except UserModel.DoesNotExist:
        extra_fields = {
            'is_staff': True
        }
        if username_field not in ('username', 'email'):
            extra_fields[username_field] = 'staff'
        user = UserModel._default_manager.create_user(
            username, 'staff@example.com', 'password', **extra_fields
        )
    return user
