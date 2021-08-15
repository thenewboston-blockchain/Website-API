from django.contrib import admin

from .models.app import App, AppImage

admin.site.register(App)
admin.site.register(AppImage)
