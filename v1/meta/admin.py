# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Responsibility, Skill


admin.site.register(Category)
admin.site.register(Responsibility)
admin.site.register(Skill)
