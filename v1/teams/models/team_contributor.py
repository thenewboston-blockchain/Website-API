# -*- coding: utf-8 -*-
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class TeamContributor(CreatedModified):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    contributor = models.ForeignKey('contributors.Contributor', on_delete=models.CASCADE)

    is_lead = models.BooleanField(default=False)
    pay_per_day = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            ('team', 'contributor'),
        )
