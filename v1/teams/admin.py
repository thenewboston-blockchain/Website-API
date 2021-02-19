from django.contrib import admin

from .models.slack_channel import SlackChannel
from .models.team import Team
from .models.team_member import TeamMember

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(SlackChannel)
