from django.db import models

from .project_team import ProjectTeam
from .team_member import TeamMember


class ProjectMember(TeamMember):
    team = models.ForeignKey(ProjectTeam, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.title}: {self.pay_per_day}'
