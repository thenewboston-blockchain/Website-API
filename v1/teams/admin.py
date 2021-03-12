from django.contrib import admin

from .models.slack_channel import SlackChannel
from .models.team import CoreTeam, ProjectTeam, Team
from .models.team_member import CoreMember, ProjectMember, TeamMember

admin.site.register(CoreTeam)
admin.site.register(ProjectTeam)
admin.site.register(Team)
admin.site.register(CoreMember)
admin.site.register(ProjectMember)
admin.site.register(TeamMember)
admin.site.register(SlackChannel)
