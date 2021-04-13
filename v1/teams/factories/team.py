import factory
from factory.django import DjangoModelFactory

from v1.users.factories.user import UserFactory
from ..models.team import CoreTeam, ProjectTeam, Team
from ..models.team_member import CoreMember, ProjectMember, TeamMember


class TeamFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)
    about = factory.Faker('text', max_nb_chars=1024)
    github = factory.Faker('pystr')
    discord = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = Team

    @ factory.post_generation
    def team_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                TeamMemberFactory.create_batch(extracted, team=self)


class CoreTeamFactory(TeamFactory):
    responsibilities = factory.Faker('pylist', nb_elements=10, variable_nb_elements=True, value_types='str')

    class Meta:
        model = CoreTeam

    @ factory.post_generation
    def core_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                CoreMemberFactory.create_batch(extracted, core_team=self)


class ProjectTeamFactory(TeamFactory):
    external_url = factory.Faker('pystr')
    is_active = factory.Faker('pybool')

    class Meta:
        model = ProjectTeam

    @ factory.post_generation
    def project_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                ProjectMemberFactory.create_batch(extracted, project_team=self)


class TeamMemberFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    is_lead = factory.Faker('pybool')
    job_title = factory.Faker('pystr', max_chars=250)
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = TeamMember


class CoreMemberFactory(TeamMemberFactory):
    hourly_rate = factory.Faker('pyint')
    weekly_hourly_commitment = factory.Faker('pyint')
    core_team = factory.SubFactory(CoreTeamFactory)

    class Meta:
        model = CoreMember


class ProjectMemberFactory(TeamMemberFactory):
    project_team = factory.SubFactory(ProjectTeamFactory)

    class Meta:
        model = ProjectMember
