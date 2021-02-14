from django.contrib import admin

from .models.playlist import Playlist
from .models.video import Video

admin.site.register(Playlist)
admin.site.register(Video)
