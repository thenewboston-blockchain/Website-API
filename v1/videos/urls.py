from rest_framework.routers import SimpleRouter

from .views.instructor import InstructorViewSet
from .views.playlist import PlaylistViewSet
from .views.playlist_category import PlaylistCategoryViewSet
from .views.video import VideoViewSet

router = SimpleRouter(trailing_slash=False)
router.register('instructors', InstructorViewSet)
router.register('playlist_categories', PlaylistCategoryViewSet)
router.register('playlists', PlaylistViewSet)
router.register('videos', VideoViewSet)
