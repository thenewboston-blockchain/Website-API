from rest_framework.routers import SimpleRouter

from .views.core_team import CoreTeamViewSet
from .views.slack_channel import SlackChannelViewSet
from .views.team import TeamViewSet
from .views.team_member import TeamMemberViewSet

router = SimpleRouter(trailing_slash=False)
router.register('teams', TeamViewSet)
router.register('core_teams', CoreTeamViewSet)
router.register('teams_members', TeamMemberViewSet)
router.register('slack_channels', SlackChannelViewSet)
