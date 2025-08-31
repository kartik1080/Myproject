from rest_framework import serializers
from .models import (
    MonitoringSession, CollectedContent, MonitoringRule, 
    MonitoringMetrics, PlatformConnection
)


class MonitoringSessionSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = MonitoringSession
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class MonitoringSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSession
        fields = ['platform', 'session_type', 'target_keywords', 'monitoring_frequency', 'description']


class CollectedContentSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = CollectedContent
        fields = '__all__'
        read_only_fields = ['id', 'collected_at', 'created_at']


class CollectedContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectedContent
        fields = ['session', 'platform', 'content_type', 'content', 'source_url', 'author', 'metadata']


class MonitoringRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringRule
        fields = '__all__'


class MonitoringMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringMetrics
        fields = '__all__'


class PlatformConnectionSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = PlatformConnection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlatformConnectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformConnection
        fields = ['platform', 'connection_type', 'credentials', 'settings', 'is_active']


class MonitoringStatsSerializer(serializers.Serializer):
    total_sessions = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    total_content_collected = serializers.IntegerField()
    content_today = serializers.IntegerField()
    sessions_by_platform = serializers.DictField()
    content_by_type = serializers.DictField()
    average_session_duration = serializers.FloatField()
    connection_status = serializers.DictField()


class RealTimeMonitoringSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    platform_name = serializers.CharField()
    status = serializers.CharField()
    last_activity = serializers.DateTimeField()
    content_count = serializers.IntegerField()
    alerts_count = serializers.IntegerField()


class BulkContentSerializer(serializers.Serializer):
    content_items = CollectedContentCreateSerializer(many=True)
    session_id = serializers.IntegerField()
    batch_id = serializers.CharField(required=False)


class MonitoringSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    platform = serializers.IntegerField(required=False)
    session_type = serializers.CharField(required=False)
    content_type = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    status = serializers.CharField(required=False)
