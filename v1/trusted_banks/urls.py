from rest_framework.routers import SimpleRouter

from .views.trusted_bank import TrustedBankViewSet

router = SimpleRouter(trailing_slash=False)
router.register('trusted_banks', TrustedBankViewSet)
