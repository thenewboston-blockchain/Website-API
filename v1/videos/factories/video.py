import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models.instructor import Instructor
from ..models.playlist import Playlist
from ..models.playlist_category import PlaylistCategory
from ..models.video import Video


class InstructorFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=250)
    youtube_url = factory.Faker('pystr')
    vimeo_url = factory.Faker('pystr')

    class Meta:
        model = Instructor


class PlaylistFactory(DjangoModelFactory):
    title = factory.Faker('pystr', max_chars=250)
    description = factory.Faker('text')
    published_at = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    instructor = factory.SubFactory(InstructorFactory)
    thumbnail = factory.Faker('pystr', max_chars=250)
    playlist_type = factory.Faker('pystr', max_chars=11)
    is_featured = factory.Faker('pybool')

    class Meta:
        model = Playlist

    @factory.post_generation
    def videos(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                VideoFactory.create_batch(extracted, playlist=self)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if not isinstance(extracted, (int, list, set, tuple)):
                return
            if isinstance(extracted, int):
                for _ in range(extracted):
                    self.categories.add(PlaylistCategoryFactory())
            else:
                for category in extracted:
                    self.categories.add(category)


class VideoFactory(DjangoModelFactory):
    video_id = factory.Faker('pystr', max_chars=11)
    title = factory.Faker('pystr', max_chars=250)
    description = factory.Faker('text')
    published_at = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    duration_seconds = factory.Faker('pyint')
    thumbnail = factory.Faker('pystr', max_chars=250)
    playlist = factory.SubFactory(PlaylistFactory)
    position = factory.Faker('pyint')

    class Meta:
        model = Video


class PlaylistCategoryFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=250)

    class Meta:
        model = PlaylistCategory
