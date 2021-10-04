from rest_framework.routers import SimpleRouter

from .views.app import AppImageViewSet, AppViewSet, CategoryViewSet

router = SimpleRouter(trailing_slash=False)
router.register('app_store/apps', AppViewSet)
router.register('app_store/images', AppImageViewSet)
router.register('app/categories', CategoryViewSet)
