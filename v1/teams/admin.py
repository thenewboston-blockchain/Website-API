from django.contrib import admin

from .models.team import Team, CoreTeam, ProjectTeam
from .models.team_member import TeamMember, CoreMember, ProjectMember

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(CoreTeam)
admin.site.register(ProjectTeam)
admin.site.register(CoreMember)
admin.site.register(ProjectMember)
