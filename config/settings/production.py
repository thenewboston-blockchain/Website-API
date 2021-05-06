import iptools

from .base import *  # noqa: F401

SENTRY_DSN = os.getenv('SENTRY_DSN')

# if SENTRY_DSN:
#     import sentry_sdk
#     from sentry_sdk.integrations.django import DjangoIntegration
#
#     sentry_sdk.init(
#         SENTRY_DSN,
#         traces_sample_rate=1.0,
#         integrations=[DjangoIntegration()],
#     )

DEBUG = False

INTERNAL_IPS = iptools.IpRangeList(
    '10/8',
    '127/8',
    '172.16/12',
    '192.168/16'
)
