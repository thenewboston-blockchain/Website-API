from rest_framework.routers import SimpleRouter

from .views.category import PlaylistCategoryViewSet
from .views.instructor import InstructorViewSet
from .views.playlist import PlaylistViewSet
from .views.video import VideoViewSet


router = SimpleRouter(trailing_slash=False)
router.register('videos', VideoViewSet)
router.register('playlists', PlaylistViewSet)
router.register('playlist_categories', PlaylistCategoryViewSet)
router.register('instructors', InstructorViewSet)
