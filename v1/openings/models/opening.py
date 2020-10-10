# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Opening(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    pay_per_day = models.PositiveIntegerField()
    eligible_for_task_points = models.BooleanField(default=False, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    reports_to = models.ManyToManyField('contributors.Contributor')

    categories = models.ManyToManyField('meta.Category')
    responsibilities = models.ManyToManyField('meta.Responsibility')
    skills = models.ManyToManyField('meta.Skill')

    def __str__(self):
        return f'#{self.pk}: {self.title}'
