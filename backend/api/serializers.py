from rest_framework import serializers
from .models import (
    APIAccessLog, APIKey, WebhookEndpoint, DataExport, SystemHealth
)


class APIAccessLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    endpoint_name = serializers.CharField(source='endpoint', read_only=True)
    
    class Meta:
        model = APIAccessLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'response_time', 'created_at']


class APIKeySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = APIKey
        fields = '__all__'
        read_only_fields = ['id', 'key', 'created_at', 'last_used']


class APIKeyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['name', 'permissions', 'expires_at', 'is_active']


class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebhookEndpointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = ['name', 'url', 'events', 'secret_key', 'is_active', 'description']


class DataExportSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DataExport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'completed_at']


class DataExportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataExport
        fields = ['export_type', 'data_source', 'format', 'filters', 'include_metadata']


class SystemHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemHealth
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'created_at']


class SystemHealthCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemHealth
        fields = ['component', 'status', 'details', 'metrics']


class APIDashboardSerializer(serializers.Serializer):
    total_requests = serializers.IntegerField()
    requests_today = serializers.IntegerField()
    average_response_time = serializers.FloatField()
    error_rate = serializers.FloatField()
    top_endpoints = serializers.ListField()
    active_api_keys = serializers.IntegerField()
    webhook_deliveries = serializers.IntegerField()
    system_health_score = serializers.FloatField()


class RealTimeAPISerializer(serializers.Serializer):
    current_requests = serializers.IntegerField()
    active_connections = serializers.IntegerField()
    recent_errors = serializers.IntegerField()
    performance_metrics = serializers.DictField()
    system_status = serializers.DictField()


class APIStatsSerializer(serializers.Serializer):
    requests_by_hour = serializers.DictField()
    requests_by_endpoint = serializers.DictField()
    requests_by_user = serializers.DictField()
    response_time_distribution = serializers.DictField()
    error_codes = serializers.DictField()


class WebhookTestSerializer(serializers.Serializer):
    endpoint_id = serializers.IntegerField()
    test_payload = serializers.DictField()
    test_event = serializers.CharField()


class BulkExportSerializer(serializers.Serializer):
    exports = DataExportCreateSerializer(many=True)
    batch_id = serializers.CharField(required=False)


class APISearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    endpoint = serializers.CharField(required=False)
    user = serializers.IntegerField(required=False)
    status_code = serializers.IntegerField(required=False)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    response_time_min = serializers.FloatField(required=False)
    response_time_max = serializers.FloatField(required=False)
