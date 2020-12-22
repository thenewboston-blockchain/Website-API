# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Opening(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    responsibilities = models.ManyToManyField('Responsibility')
    skills = models.ManyToManyField('Skill')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)

    active = models.BooleanField(default=True, db_index=True)
    description = models.TextField()
    eligible_for_task_points = models.BooleanField(default=False, db_index=True)
    pay_per_day = models.PositiveIntegerField()
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    class Meta:
        ordering = ('created_date',)
