from django.contrib import admin

from .models.team import Team
from .models.team_member import TeamMember

admin.site.register(Team)
admin.site.register(TeamMember)
