from django.contrib import admin

from .models.instructor import Instructor
from .models.playlist import Playlist
from .models.playlist_category import PlaylistCategory
from .models.video import Video

admin.site.register(Instructor)
admin.site.register(Playlist)
admin.site.register(PlaylistCategory)
admin.site.register(Video)
