from django.contrib import admin

from .models.community import Community
from .models.economy import Economy

admin.site.register(Community)
admin.site.register(Economy)
