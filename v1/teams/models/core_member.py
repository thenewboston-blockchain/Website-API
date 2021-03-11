from django.db import models

from .core_team import CoreTeam
from .team_member import TeamMember


class CoreMember(TeamMember):
    pay_per_day = models.PositiveIntegerField(default=2800)
    team = models.ForeignKey(CoreTeam, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.title}: {self.pay_per_day}'
