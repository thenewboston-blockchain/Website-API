import factory
from factory.django import DjangoModelFactory

from ..models.roadmap import Roadmap
from ...teams.factories.team import CoreTeamFactory


class RoadmapFactory(DjangoModelFactory):
    team = factory.SubFactory(CoreTeamFactory)
    task_title = factory.Faker('pystr', max_chars=250)
    estimated_completion_date = factory.Faker('date')
    is_complete = factory.Faker('pybool')

    class Meta:
        model = Roadmap
