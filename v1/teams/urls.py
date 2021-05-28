from rest_framework.routers import SimpleRouter

from .views.team import CoreTeamViewSet, ProjectTeamViewSet, TeamViewSet
from .views.team_member import CoreMemberViewSet, ProjectMemberViewSet, TeamMemberViewSet

router = SimpleRouter(trailing_slash=False)
router.register('core_members', CoreMemberViewSet)
router.register('core_teams', CoreTeamViewSet)
router.register('project_members', ProjectMemberViewSet)
router.register('project_teams', ProjectTeamViewSet)
router.register('teams', TeamViewSet)
router.register('teams_members', TeamMemberViewSet)
