# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Task(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    contributor = models.ForeignKey('team.Contributor', on_delete=models.CASCADE)
    repository = models.CharField(max_length=250)
    completed_date = models.DateTimeField(null=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'#{self.pk}: {self.title}'
