import factory
from factory.django import DjangoModelFactory, ImageField

from ..models.app import App, AppImage


class AppFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)
    description = factory.Faker('text')
    logo = ImageField(width=1024, height=768)
    website = factory.Faker('url')

    class Meta:
        model = App

    @factory.post_generation
    def images(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.images.add(AppImageFactory())
            else:
                for entry in extracted:
                    self.images.add(entry)


class AppImageFactory(DjangoModelFactory):
    app = factory.SubFactory(AppFactory)
    image = ImageField(width=1024, height=768)

    class Meta:
        model = AppImage
