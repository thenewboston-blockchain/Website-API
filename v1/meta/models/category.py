# -*- coding: utf-8 -*-
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Category(CreatedModified):
    title = models.CharField(max_length=250)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
