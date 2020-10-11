# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Task(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    contributor = models.ForeignKey('contributors.Contributor', on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()
    completed_date = models.DateTimeField(null=True)
    repository = models.CharField(max_length=250)
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
