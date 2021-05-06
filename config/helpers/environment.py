import os

ENVIRONMENT = os.environ['DJANGO_APPLICATION_ENVIRONMENT']

if ENVIRONMENT == 'local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'postgres_local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'dev':
    SETTINGS_MODULE = 'config.settings.dev'

if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'config.settings.production'

if ENVIRONMENT == 'test':
    SETTINGS_MODULE = 'config.settings.test'
