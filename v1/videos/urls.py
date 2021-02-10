from rest_framework.routers import SimpleRouter

from .views.video import VideoViewSet
from .views.playlist import PlaylistViewSet

router = SimpleRouter(trailing_slash=False)
router.register('videos', VideoViewSet)
router.register('playlists', PlaylistViewSet)
