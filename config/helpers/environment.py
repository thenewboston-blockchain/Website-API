# -*- coding: utf-8 -*-
import os

ENVIRONMENT = os.environ['DJANGO_APPLICATION_ENVIRONMENT']

if ENVIRONMENT == 'local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'postgres_local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'config.settings.production'
