from django.contrib import admin

from .models.analytics import AnalyticsCategory, AnalyticsData, Analytics

admin.site.register(AnalyticsCategory)
admin.site.register(AnalyticsData)
admin.site.register(Analytics)
