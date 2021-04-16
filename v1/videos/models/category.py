import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Category(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'#{self.pk}: {self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('created_date',)
