import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.milestone import Milestone
from ..models.project import Project
from ...teams.factories.team import ProjectMemberFactory


class ProjectFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)
    project_lead = factory.SubFactory(ProjectMemberFactory)
    description = factory.Faker('text')
    logo = factory.Faker('pystr', max_chars=200)
    github_url = factory.Faker('pystr', max_chars=200)
    overview = factory.Faker('text')
    problem = factory.Faker('text')
    target_market = factory.Faker('text')
    benefits = factory.Faker('text')
    centered_around_tnb = factory.Faker('text')
    estimated_completion_date = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    is_featured = factory.Faker('pybool')

    class Meta:
        model = Project


class MilestoneFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    number = factory.Faker('pyint')
    description = factory.Faker('text')

    class Meta:
        model = Milestone
