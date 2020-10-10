# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified

from v1.teams.models import Team


class Opening(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reports_to = models.ManyToManyField('contributors.Contributor')
    responsibilities = models.ManyToManyField('meta.Responsibility')
    skills = models.ManyToManyField('meta.Skill')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    active = models.BooleanField(default=True, db_index=True)
    description = models.TextField()
    eligible_for_task_points = models.BooleanField(default=False, db_index=True)
    pay_per_day = models.PositiveIntegerField()
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
