from django.contrib import admin

from .models.analytics import Analytics, AnalyticsCategory, AnalyticsData

admin.site.register(AnalyticsCategory)
admin.site.register(AnalyticsData)
admin.site.register(Analytics)
