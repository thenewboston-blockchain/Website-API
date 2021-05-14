from django.contrib import admin

from .models.category import PlaylistCategory
from .models.instructor import Instructor
from .models.playlist import Playlist
from .models.video import Video

admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(PlaylistCategory)
admin.site.register(Instructor)
