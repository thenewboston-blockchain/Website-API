from rest_framework.routers import SimpleRouter

from .views.team import TeamViewSet
from .views.team_member import TeamMemberViewSet
from .views.slack_channel import SlackChannelViewSet

router = SimpleRouter(trailing_slash=False)
router.register('teams', TeamViewSet)
router.register('teams_members', TeamMemberViewSet)
router.register('slack_channels', SlackChannelViewSet)
