# -*- coding: utf-8 -*-
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    PositiveBigIntegerField,
    TextChoices,
    UUIDField,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _
from thenewboston.constants.network import MAX_POINT_VALUE, MIN_POINT_VALUE
from thenewboston.models.created_modified import CreatedModified

from v1.repositories.models.repository import Repository


class UserEarnings(CreatedModified):
    class TimePeriod(TextChoices):
        ALL = 'all', _('All')
        SEVEN_DAYS = '7d', _('7 Days')
        THIRTY_DAYS = '30d', _('30 Days')

    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = ForeignKey('users.User', on_delete=CASCADE)

    repository = ForeignKey(Repository, on_delete=CASCADE)
    time_period = CharField(max_length=8, choices=TimePeriod.choices)
    total_amount = PositiveBigIntegerField(
        validators=[
            MaxValueValidator(MAX_POINT_VALUE),
            MinValueValidator(MIN_POINT_VALUE),
        ]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['repository', 'time_period', 'user'],
                name='unique_repository_time_period_user'
            )
        ]
        default_related_name = 'user_earnings'
        verbose_name_plural = 'user earnings'

    def __str__(self):
        return f'#{self.pk}: {self.user.email}/{self.repository}/{self.time_period}'
