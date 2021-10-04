from django.contrib import admin

from .models.app import App, AppImage, Category

admin.site.register(App)
admin.site.register(AppImage)
admin.site.register(Category)
