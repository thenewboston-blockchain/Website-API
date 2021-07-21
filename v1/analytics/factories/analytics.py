import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.analytics import Analytics, AnalyticsCategory, AnalyticsData


class AnalyticsFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = Analytics

    @factory.post_generation
    def data(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.data.add(AnalyticsDataFactory())
            else:
                for entry in extracted:
                    self.data.add(entry)


class AnalyticsCategoryFactory(DjangoModelFactory):
    key = factory.Faker('pystr', max_chars=255)
    title = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = AnalyticsCategory

    @factory.post_generation
    def analytics(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.analytics.add(AnalyticsFactory())
            else:
                for entry in extracted:
                    self.analytics.add(entry)


class AnalyticsDataFactory(DjangoModelFactory):
    analytics = factory.SubFactory(AnalyticsFactory)
    date = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    value = factory.Faker('pyint')

    class Meta:
        model = AnalyticsData
