from django.contrib import admin

from .models.community import Community
from .models.economy import Economy
from .models.network import Network

admin.site.register(Community)
admin.site.register(Economy)
admin.site.register(Network)
