from rest_framework.serializers import ModelSerializer

from ..models.analytics import Analytics, AnalyticsCategory, AnalyticsData


class AnalyticsCategorySerializer(ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'created_date',
            'modified_date',
            'key',
            'title',
            'analytics',
        )
        model = AnalyticsCategory
        read_only_fields = 'created_date', 'modified_date'
        depth = 2


class AnalyticsCategorySerializerCreate(ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'created_date',
            'modified_date',
            'key',
            'title',
            'analytics',
        )
        model = AnalyticsCategory
        read_only_fields = 'created_date', 'modified_date'


class AnalyticsSerializer(ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'created_date',
            'modified_date',
            'title',
            'data',
        )
        model = Analytics
        read_only_fields = 'created_date', 'modified_date'
        depth = 1


class AnalyticsDataSerializer(ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'created_date',
            'modified_date',
            'analytics',
            'date',
            'value'
        )
        model = AnalyticsData
        read_only_fields = 'created_date', 'modified_date'
