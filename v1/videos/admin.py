from django.contrib import admin

from .models.category import Category
from .models.playlist import Playlist
from .models.video import Video

admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Category)
