# -*- coding: utf-8 -*-
from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
