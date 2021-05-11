from .base import *

SENTRY_DSN = os.getenv('SENTRY_DSN')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        SENTRY_DSN,
        traces_sample_rate=1.0,
        integrations=[DjangoIntegration()],
    )

DEBUG = False

INTERNAL_IPS = [
    '127.0.0.1',
]
