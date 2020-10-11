# -*- coding: utf-8 -*-
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Responsibility(CreatedModified):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'responsibility'
        verbose_name_plural = 'responsibilities'

    def __str__(self):
        return f'#{self.pk}: {self.title}'
