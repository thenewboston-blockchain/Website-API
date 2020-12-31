from django.contrib import admin

from .models.opening import Opening
from .models.responsibility import Responsibility
from .models.skill import Skill

admin.site.register(Opening)
admin.site.register(Responsibility)
admin.site.register(Skill)
