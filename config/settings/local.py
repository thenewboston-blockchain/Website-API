# -*- coding: utf-8 -*-
import iptools

from .base import *

DEBUG = True

INTERNAL_IPS = iptools.IpRangeList(
    '10/8',
    '127/8',
    '172.16/12',
    '192.168/16'
)

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST", "localhost")}:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'thenewboston',
        'USER': 'thenewboston',
        'PASSWORD': 'thenewboston',
        'HOST': 'db',
        'PORT': '5432'
    }
}
