from django.contrib import admin

from .models.analytics import AnalyticsCategory, AnalyticsData, AnalyticsType

admin.site.register(AnalyticsCategory)
admin.site.register(AnalyticsData)
admin.site.register(AnalyticsType)
