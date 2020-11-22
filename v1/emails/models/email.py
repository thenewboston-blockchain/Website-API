# -*- coding: utf-8 -*-
from django.db import models


class Email(models.Model):
    email = models.EmailField(max_length=250, blank=False, unique=True)
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.pk}: {self.email}'
