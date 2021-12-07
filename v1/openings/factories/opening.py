import factory
from factory.django import DjangoModelFactory

from v1.teams.factories.team import TeamFactory
from .responsibility import ResponsibilityFactory
from .skill import SkillFactory
from ..models.opening import Opening


class OpeningFactory(DjangoModelFactory):
    active = factory.Faker('pybool')
    description = factory.Faker('text', max_nb_chars=1024)
    team = factory.SubFactory(TeamFactory)
    title = factory.Faker('pystr', max_chars=250)
    visible = factory.Faker('pybool')
    application_form = factory.Faker('pystr', max_chars=255)
    category = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = Opening

    @factory.post_generation
    def responsibilities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.responsibilities.add(ResponsibilityFactory())
            else:
                for responsibility in extracted:
                    self.responsibilities.add(responsibility)

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.skills.add(SkillFactory())
            else:
                for skill in extracted:
                    self.skills.add(skill)
