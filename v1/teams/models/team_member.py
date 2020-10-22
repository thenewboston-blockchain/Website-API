# -*- coding: utf-8 -*-
import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class TeamMember(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    is_lead = models.BooleanField(default=False)
    pay_per_day = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            ('team', 'user'),
        )
