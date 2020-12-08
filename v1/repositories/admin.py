# -*- coding: utf-8 -*-
from django.contrib import admin

from .models.repository import Repository

admin.site.register(Repository)
