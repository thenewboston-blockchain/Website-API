import factory
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory

from ..models.app import App, AppImage


class AppFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)
    description = factory.Faker('text')
    logo = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 200, 'height': 200}
            ), 'example.jpg'
        )
    )
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
    image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 200, 'height': 200}
            ), 'example.jpg'
        )
    )

    class Meta:
        model = AppImage
