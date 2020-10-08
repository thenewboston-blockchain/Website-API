# -*- coding: utf-8 -*-
from django.conf import settings
import pytest
from pytest_django.migrations import DisableMigrations
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


@pytest.fixture(scope='session', autouse=True)
def migrations_disabled():
    settings.MIGRATION_MODULES = DisableMigrations()
    yield None


@pytest.fixture()
def api_client():
    return APIClient()
