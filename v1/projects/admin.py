from django.contrib import admin

from .models.milestone import Milestone
from .models.project import Project

admin.site.register(Project)
admin.site.register(Milestone)
