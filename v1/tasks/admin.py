# -*- coding: utf-8 -*-
from django.contrib import admin

from .models.task import Task

admin.site.register(Task)
