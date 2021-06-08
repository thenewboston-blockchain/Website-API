from rest_framework.routers import SimpleRouter

from .views.feedback import FeedbackViewSet

router = SimpleRouter(trailing_slash=False)
router.register('feedback', FeedbackViewSet)
