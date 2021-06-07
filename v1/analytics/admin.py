from django.contrib import admin

from .models.community import Community
from .models.economy import Economy
from .models.facebook import Facebook
from .models.instagram import Instagram
from .models.linkedin import LinkedIn
from .models.network import Network
from .models.twitter import Twitter


admin.site.register(Community)
admin.site.register(Economy)
admin.site.register(Facebook)
admin.site.register(Instagram)
admin.site.register(LinkedIn)
admin.site.register(Network)
admin.site.register(Twitter)
