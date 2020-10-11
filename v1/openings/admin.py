# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Opening, Responsibility, Skill

admin.site.register(Opening)
admin.site.register(Responsibility)
admin.site.register(Skill)
