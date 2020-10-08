# -*- coding: utf-8 -*-
import pytest


@pytest.mark.django_db
def test_migration():
    """Will run migration"""
    assert True
