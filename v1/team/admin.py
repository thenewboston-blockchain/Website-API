# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Contributor, Team


admin.site.register(Team)
admin.site.register(Contributor)
