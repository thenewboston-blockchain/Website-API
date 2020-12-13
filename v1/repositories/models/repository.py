# -*- coding: utf-8 -*-
import uuid

from django.db.models import CharField, URLField, UUIDField
from thenewboston.models.created_modified import CreatedModified


class Repository(CreatedModified):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = URLField(blank=True)
    display_name = CharField(max_length=80, unique=True)  # TNB-python-client

    def __str__(self):
        return f'#{self.pk}: {self.url} ({self.display_name})'
