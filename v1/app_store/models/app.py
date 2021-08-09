import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class App(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='media/images/app_store')
    website = models.URLField()
    images = models.ManyToManyField('AppImage', blank=True, related_name='app_images')

    def __str__(self):
        return f'#{self.pk}: {self.name}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(App, self).save(*args, **kwargs)


class AppImage(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    app = models.ForeignKey('App', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/app_store')

    def __str__(self):
        return f'#{self.pk}: {self.app} - {self.image}'
