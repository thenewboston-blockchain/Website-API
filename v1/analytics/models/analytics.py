import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class AnalyticsCategory(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    key = models.CharField(max_length=255)  # economy
    title = models.CharField(max_length=255)  # Economy
    analytics = models.ManyToManyField('analytics.Analytics', blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = ('analytics_category')
        verbose_name_plural = 'analytics categories'

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(AnalyticsCategory, self).save(*args, **kwargs)


class Analytics(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255)  # Total Coins Distributed to Core
    data = models.ManyToManyField('analytics.AnalyticsData', blank=True, related_name='analytics_data')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'analytics'

    def __str__(self):
        category = AnalyticsCategory.objects.get(analytics__in=[self.pk])
        category_title = ': ' + category.title if category else ''
        return f'#{self.pk} {category_title} : {self.title}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Analytics, self).save(*args, **kwargs)


class AnalyticsData(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    analytics = models.ForeignKey('analytics.Analytics', on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.PositiveIntegerField()

    class Meta:
        ordering = ('date',)
        verbose_name = ('analytics_data')
        verbose_name_plural = 'analytics data'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(AnalyticsData, self).save(*args, **kwargs)

    def __str__(self):
        return f'#{self.pk}: {self.date}'
