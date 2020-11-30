# -*- coding: utf-8 -*-
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from thenewboston.constants.network import MAX_POINT_VALUE, MIN_POINT_VALUE
from thenewboston.models.created_modified import CreatedModified


class Product(CreatedModified):
    class Status(models.TextChoices):
        ARCHIVED = 'archived', _('Archived')
        DECLINED = 'declined', _('Declined')
        DRAFT = 'draft', _('Draft')
        PENDING_REVIEW = 'pending_review', _('Pending Review')
        PUBLISHED = 'published', _('Published')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
    price = models.PositiveBigIntegerField(
        validators=[
            MaxValueValidator(MAX_POINT_VALUE),
            MinValueValidator(MIN_POINT_VALUE),
        ]
    )
    published_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=14, choices=Status.choices)
    title = models.CharField(max_length=128)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
