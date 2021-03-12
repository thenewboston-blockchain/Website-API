import factory
from factory.django import DjangoModelFactory

from v1.users.factories.user import UserFactory
from ..models.slack_channel import SlackChannel
from ..models.team import CoreTeam, ProjectTeam, Team
from ..models.team_member import CoreMember, TeamMember


class TeamFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)
    about = factory.Faker('text', max_nb_chars=1024)
    github = factory.Faker('pystr')
    slack = factory.Faker('pystr', max_chars=250)

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
    responsibilities = factory.Faker('text', max_nb_chars=1024)

    class Meta:
        model = CoreTeam


class ProjectTeamFactory(TeamFactory):
    external_url = factory.Faker('pystr')
    is_active = factory.Faker('pybool')

    class Meta:
        model = ProjectTeam


class TeamMemberFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    is_lead = factory.Faker('pybool')
    job_title = factory.Faker('pystr', max_chars=250)
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = TeamMember


class CoreMemberFactory(TeamMemberFactory):
    pay_per_day = factory.Faker('pyint')

    class Meta:
        model = CoreMember


class SlackChannelFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=250)
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = SlackChannel
