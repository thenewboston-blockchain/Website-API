from rest_framework.routers import SimpleRouter

from .views.app import AppImageViewSet, AppViewSet

router = SimpleRouter(trailing_slash=False)
router.register('app_store/apps', AppViewSet)
router.register('app_store/images', AppImageViewSet)
