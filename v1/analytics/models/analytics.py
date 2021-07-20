import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class AnalyticsCategory(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    key = models.CharField(max_length=255)  # economy
    title = models.CharField(max_length=255)  # Economy
    analytics = models.ManyToManyField('analytics.AnalyticsType', blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = ('analytics_category')
        verbose_name_plural = 'analytics categories'

    def __str__(self):
        return f'#{self.pk}: {self.title}'


class AnalyticsType(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255)  # Total Coins Distributed to Core
    data = models.ManyToManyField('analytics.AnalyticsData', blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = ('analytics_type')
        verbose_name_plural = 'analytics types'

    def __str__(self):
        return f'#{self.pk}: {self.title}'


class AnalyticsData(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    analytics = models.ForeignKey('analytics.AnalyticsType', on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.PositiveIntegerField()

    class Meta:
        ordering = ('date',)
        verbose_name = ('analytics_data')
        verbose_name_plural = 'analytics data'

    def __str__(self):
        return f'#{self.pk}: {self.date}'
