import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.facebook import Facebook


class FacebookFactory(DjangoModelFactory):
    actions_on_page = factory.Faker('pyint')
    page_views = factory.Faker('pyint')
    page_likes = factory.Faker('pyint')
    post_reach = factory.Faker('pyint')
    story_reach = factory.Faker('pyint')
    recommendations = factory.Faker('pyint')
    post_engagement = factory.Faker('pyint')
    responsiveness = factory.Faker('pyint')
    videos = factory.Faker('pyint')
    followers = factory.Faker('pyint')
    week_ending = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Facebook
