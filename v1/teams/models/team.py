# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Team(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team_members = models.ManyToManyField('users.User', through='TeamMember')

    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
