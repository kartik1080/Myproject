from rest_framework import serializers
from .models import (
    AnalyticsReport, TrendAnalysis, GeographicAnalysis, 
    UserBehaviorAnalysis, PerformanceMetrics, AlertMetrics
)


class AnalyticsReportSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = AnalyticsReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnalyticsReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsReport
        fields = ['report_type', 'date_range', 'parameters', 'description']


class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = '__all__'


class GeographicAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicAnalysis
        fields = '__all__'


class UserBehaviorAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBehaviorAnalysis
        fields = '__all__'


class PerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetrics
        fields = '__all__'


class AlertMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertMetrics
        fields = '__all__'


class AnalyticsDashboardSerializer(serializers.Serializer):
    total_reports = serializers.IntegerField()
    reports_this_month = serializers.IntegerField()
    average_report_generation_time = serializers.FloatField()
    top_report_types = serializers.ListField()
    recent_trends = serializers.DictField()
    geographic_hotspots = serializers.ListField()
    user_behavior_insights = serializers.DictField()
    performance_scores = serializers.DictField()
    alert_summary = serializers.DictField()


class RealTimeAnalyticsSerializer(serializers.Serializer):
    current_detections = serializers.IntegerField()
    active_monitoring_sessions = serializers.IntegerField()
    recent_alerts = serializers.IntegerField()
    system_performance = serializers.DictField()
    live_metrics = serializers.DictField()


class DataVisualizationSerializer(serializers.Serializer):
    chart_type = serializers.CharField()
    data = serializers.DictField()
    options = serializers.DictField()
    filters = serializers.DictField()


class ExportDataSerializer(serializers.Serializer):
    data_type = serializers.CharField()
    format = serializers.CharField()
    date_range = serializers.CharField()
    filters = serializers.DictField()
    include_metadata = serializers.BooleanField()


class BulkAnalyticsSerializer(serializers.Serializer):
    reports = AnalyticsReportCreateSerializer(many=True)
    batch_id = serializers.CharField(required=False)


class AnalyticsSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    report_type = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    created_by = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
