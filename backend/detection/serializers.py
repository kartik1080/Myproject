from rest_framework import serializers
from .models import (
    DrugCategory, DetectionPattern, Platform, DetectionResult,
    DetectionAnalytics, DetectionRule
)


class DrugCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugCategory
        fields = '__all__'


class DetectionPatternSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = DetectionPattern
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class DetectionResultSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    pattern_name = serializers.CharField(source='pattern.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = DetectionResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DetectionResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = ['category', 'pattern', 'platform', 'content', 'confidence_score', 'location', 'metadata']


class DetectionResultUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = ['status', 'assigned_to', 'review_notes', 'escalation_level', 'false_positive_reason']


class DetectionAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionAnalytics
        fields = '__all__'


class DetectionRuleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = DetectionRule
        fields = '__all__'


class DetectionStatsSerializer(serializers.Serializer):
    total_detections = serializers.IntegerField()
    pending_review = serializers.IntegerField()
    confirmed_detections = serializers.IntegerField()
    false_positives = serializers.IntegerField()
    detections_by_category = serializers.DictField()
    detections_by_platform = serializers.DictField()
    average_confidence = serializers.FloatField()
    recent_detections = serializers.IntegerField()


class BulkDetectionSerializer(serializers.Serializer):
    detections = DetectionResultCreateSerializer(many=True)
    platform_id = serializers.IntegerField()
    batch_id = serializers.CharField(required=False)


class DetectionSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    category = serializers.IntegerField(required=False)
    platform = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    confidence_min = serializers.FloatField(required=False)
    confidence_max = serializers.FloatField(required=False)
