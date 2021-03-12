from rest_framework.routers import SimpleRouter

from .views.slack_channel import SlackChannelViewSet
from .views.team import CoreTeamViewSet, ProjectTeamViewSet, TeamViewSet
from .views.team_member import CoreMemberViewSet, TeamMemberViewSet

router = SimpleRouter(trailing_slash=False)
router.register('teams', TeamViewSet)
router.register('core_teams', CoreTeamViewSet)
router.register('project_teams', ProjectTeamViewSet)
router.register('core_members', CoreMemberViewSet)
router.register('teams_members', TeamMemberViewSet)
router.register('slack_channels', SlackChannelViewSet)
