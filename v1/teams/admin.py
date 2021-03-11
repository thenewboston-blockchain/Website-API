from django.contrib import admin

from .models.core_member import CoreMember
from .models.core_team import CoreTeam
from .models.project_member import ProjectMember
from .models.project_team import ProjectTeam
from .models.team import Team
from .models.team_member import TeamMember


admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(CoreTeam)
admin.site.register(ProjectTeam)
admin.site.register(CoreMember)
admin.site.register(ProjectMember)
