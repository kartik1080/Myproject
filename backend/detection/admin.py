"""
Admin configuration for detection app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    DrugCategory, DetectionPattern, Platform, DetectionResult, 
    DetectionAnalytics, DetectionRule
)


@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    """
    Admin for DrugCategory model.
    """
    list_display = [
        'name', 'risk_level', 'is_active', 'detection_count', 'created_at'
    ]
    list_filter = ['risk_level', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['risk_level', 'name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'risk_level')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def detection_count(self, obj):
        """Display count of detections for this category."""
        count = DetectionResult.objects.filter(
            detection_pattern__drug_categories=obj
        ).count()
        return count
    detection_count.short_description = 'Detections'


@admin.register(DetectionPattern)
class DetectionPatternAdmin(admin.ModelAdmin):
    """
    Admin for DetectionPattern model.
    """
    list_display = [
        'name', 'pattern_type', 'confidence_threshold', 'priority', 
        'is_active', 'last_used', 'drug_categories_display'
    ]
    list_filter = [
        'pattern_type', 'is_active', 'priority', 'created_at'
    ]
    search_fields = ['name', 'description', 'pattern_data']
    ordering = ['-priority', 'name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'pattern_type')
        }),
        ('Pattern Data', {
            'fields': ('pattern_data',)
        }),
        ('Settings', {
            'fields': ('confidence_threshold', 'priority', 'is_active')
        }),
        ('Categories', {
            'fields': ('drug_categories',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_used']
    filter_horizontal = ['drug_categories']
    
    def drug_categories_display(self, obj):
        """Display drug categories as comma-separated list."""
        categories = obj.drug_categories.all()
        if categories:
            return ', '.join([cat.name for cat in categories])
        return 'None'
    drug_categories_display.short_description = 'Drug Categories'


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    """
    Admin for Platform model.
    """
    list_display = [
        'name', 'platform_type', 'is_active', 'monitoring_enabled',
        'total_detections', 'last_monitoring', 'connection_status'
    ]
    list_filter = [
        'platform_type', 'is_active', 'monitoring_enabled', 'created_at'
    ]
    search_fields = ['name', 'api_endpoint']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'platform_type', 'description')
        }),
        ('API Configuration', {
            'fields': ('api_endpoint', 'api_key', 'api_secret')
        }),
        ('Settings', {
            'fields': ('is_active', 'monitoring_enabled', 'rate_limit')
        }),
        ('Statistics', {
            'fields': ('total_detections', 'last_monitoring')
        }),
    )
    
    readonly_fields = [
        'created_at', 'updated_at', 'total_detections', 'last_monitoring'
    ]
    
    def connection_status(self, obj):
        """Display connection status with color coding."""
        try:
            connection = obj.connection
            if connection.status == 'connected':
                return format_html(
                    '<span style="color: green;">● Connected</span>'
                )
            elif connection.status == 'connecting':
                return format_html(
                    '<span style="color: orange;">● Connecting</span>'
                )
            elif connection.status == 'error':
                return format_html(
                    '<span style="color: red;">● Error</span>'
                )
            else:
                return format_html(
                    '<span style="color: gray;">● Disconnected</span>'
                )
        except:
            return format_html('<span style="color: gray;">● Unknown</span>')
    connection_status.short_description = 'Connection Status'


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    """
    Admin for DetectionResult model.
    """
    list_display = [
        'id', 'platform', 'severity_level', 'status', 'assigned_to',
        'confidence_score', 'detected_at', 'content_preview'
    ]
    list_filter = [
        'platform', 'severity_level', 'status', 'detected_at',
        'assigned_to', 'reviewed_by'
    ]
    search_fields = [
        'content_text', 'username', 'user_id', 'content_id'
    ]
    ordering = ['-detected_at']
    
    fieldsets = (
        ('Detection Info', {
            'fields': ('platform', 'detection_pattern', 'confidence_score', 'severity_level')
        }),
        ('Content', {
            'fields': ('content_text', 'content_url', 'content_id')
        }),
        ('User Info', {
            'fields': ('user_id', 'username', 'user_metadata')
        }),
        ('Analysis', {
            'fields': ('detected_keywords', 'ml_predictions')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to', 'reviewed_by')
        }),
        ('Metadata', {
            'fields': ('location_data', 'device_info', 'ip_addresses')
        }),
        ('Timestamps', {
            'fields': ('detected_at', 'reviewed_at', 'resolved_at')
        }),
    )
    
    readonly_fields = [
        'detected_at', 'reviewed_at', 'resolved_at'
    ]
    
    actions = [
        'assign_to_investigator', 'mark_reviewed', 'escalate_detection',
        'mark_false_positive'
    ]
    
    def content_preview(self, obj):
        """Display content preview."""
        if obj.content_text:
            preview = obj.content_text[:100]
            if len(obj.content_text) > 100:
                preview += '...'
            return preview
        return 'No content'
    content_preview.short_description = 'Content Preview'
    
    def assign_to_investigator(self, request, queryset):
        """Assign detections to current user."""
        updated = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{updated} detections were assigned to you.')
    assign_to_investigator.short_description = "Assign to me"
    
    def mark_reviewed(self, request, queryset):
        """Mark detections as reviewed."""
        for detection in queryset:
            detection.mark_reviewed(request.user)
        updated = queryset.count()
        self.message_user(request, f'{updated} detections were marked as reviewed.')
    mark_reviewed.short_description = "Mark as reviewed"
    
    def escalate_detection(self, request, queryset):
        """Escalate detections."""
        for detection in queryset:
            detection.escalate(request.user)
        updated = queryset.count()
        self.message_user(request, f'{updated} detections were escalated.')
    escalate_detection.short_description = "Escalate detections"
    
    def mark_false_positive(self, request, queryset):
        """Mark detections as false positives."""
        for detection in queryset:
            detection.mark_reviewed(request.user, 'false_positive')
        updated = queryset.count()
        self.message_user(request, f'{updated} detections were marked as false positives.')
    mark_false_positive.short_description = "Mark as false positive"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'platform', 'detection_pattern', 'assigned_to', 'reviewed_by'
        )


@admin.register(DetectionAnalytics)
class DetectionAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin for DetectionAnalytics model.
    """
    list_display = [
        'date', 'total_detections', 'telegram_detections', 'instagram_detections',
        'whatsapp_detections', 'twitter_detections', 'avg_confidence_score'
    ]
    list_filter = ['date']
    ordering = ['-date']
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Platform Counts', {
            'fields': (
                'telegram_detections', 'instagram_detections', 'whatsapp_detections',
                'twitter_detections', 'other_detections'
            )
        }),
        ('Severity Counts', {
            'fields': (
                'low_severity', 'medium_severity', 'high_severity', 'critical_severity'
            )
        }),
        ('Status Counts', {
            'fields': (
                'pending_review', 'confirmed', 'false_positives', 'escalated'
            )
        }),
        ('Performance Metrics', {
            'fields': (
                'avg_confidence_score', 'detection_rate', 'false_positive_rate'
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DetectionRule)
class DetectionRuleAdmin(admin.ModelAdmin):
    """
    Admin for DetectionRule model.
    """
    list_display = [
        'name', 'rule_type', 'is_active', 'priority', 'last_executed'
    ]
    list_filter = ['rule_type', 'is_active', 'priority', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-priority', 'name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'rule_type')
        }),
        ('Configuration', {
            'fields': ('conditions', 'actions')
        }),
        ('Settings', {
            'fields': ('is_active', 'priority')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_executed']
