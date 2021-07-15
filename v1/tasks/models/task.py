import uuid

from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from thenewboston.constants.network import MAX_POINT_VALUE, MIN_POINT_VALUE
from thenewboston.models.created_modified import CreatedModified


class Task(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    amount = models.PositiveBigIntegerField(
        validators=[
            MaxValueValidator(MAX_POINT_VALUE),
            MinValueValidator(MIN_POINT_VALUE),
        ]
    )
    completed_date = models.DateTimeField(null=True)
    repository = models.CharField(max_length=250)
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Task, self).save(*args, **kwargs)
