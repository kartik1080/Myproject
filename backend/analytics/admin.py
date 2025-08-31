"""
Admin configuration for analytics app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    AnalyticsReport, TrendAnalysis, GeographicAnalysis, 
    UserBehaviorAnalysis, PerformanceMetrics, AlertMetrics
)


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    """
    Admin for AnalyticsReport model.
    """
    list_display = [
        'name', 'report_type', 'format', 'generated_by', 'generation_status',
        'file_size_display', 'created_at'
    ]
    list_filter = [
        'report_type', 'format', 'generation_status', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'generated_by__username'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Report Info', {
            'fields': ('name', 'description', 'report_type', 'format')
        }),
        ('Parameters', {
            'fields': ('parameters',)
        }),
        ('Generation', {
            'fields': ('generated_by', 'generation_status')
        }),
        ('Results', {
            'fields': ('file_path', 'file_size', 'content_summary')
        }),
        ('Timing', {
            'fields': ('generation_started', 'generation_completed')
        }),
    )
    
    readonly_fields = [
        'generation_started', 'generation_completed', 'created_at', 'updated_at'
    ]
    
    actions = ['regenerate_reports', 'download_reports']
    
    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.1f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.1f} MB"
        return 'N/A'
    file_size_display.short_description = 'File Size'
    
    def regenerate_reports(self, request, queryset):
        """Regenerate selected reports."""
        for report in queryset:
            report.generation_status = 'pending'
            report.save()
        updated = queryset.count()
        self.message_user(request, f'{updated} reports were queued for regeneration.')
    regenerate_reports.short_description = "Regenerate reports"
    
    def download_reports(self, request, queryset):
        """Download selected reports."""
        # This would implement actual file download
        updated = queryset.count()
        self.message_user(request, f'Download initiated for {updated} reports.')
    download_reports.short_description = "Download reports"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('generated_by')


@admin.register(TrendAnalysis)
class TrendAnalysisAdmin(admin.ModelAdmin):
    """
    Admin for TrendAnalysis model.
    """
    list_display = [
        'metric_name', 'metric_type', 'trend_direction', 'trend_strength',
        'start_date', 'end_date', 'period_type'
    ]
    list_filter = [
        'metric_type', 'trend_direction', 'period_type', 'start_date', 'end_date'
    ]
    search_fields = ['metric_name', 'metric_type']
    ordering = ['-end_date', 'metric_type']
    
    fieldsets = (
        ('Metric Info', {
            'fields': ('metric_type', 'metric_name')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'period_type')
        }),
        ('Analysis Results', {
            'fields': ('data_points', 'trend_direction', 'trend_strength')
        }),
        ('Statistical Measures', {
            'fields': ('mean_value', 'median_value', 'standard_deviation', 'correlation_coefficient')
        }),
        ('Insights', {
            'fields': ('key_insights', 'recommendations')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GeographicAnalysis)
class GeographicAnalysisAdmin(admin.ModelAdmin):
    """
    Admin for GeographicAnalysis model.
    """
    list_display = [
        'country', 'region', 'city', 'total_detections', 'unique_users',
        'risk_level', 'risk_score', 'analysis_date'
    ]
    list_filter = [
        'country', 'risk_level', 'analysis_date'
    ]
    search_fields = ['country', 'region', 'city']
    ordering = ['-total_detections', 'country']
    
    fieldsets = (
        ('Location', {
            'fields': ('country', 'region', 'city')
        }),
        ('Activity Metrics', {
            'fields': ('total_detections', 'unique_users', 'active_channels')
        }),
        ('Risk Assessment', {
            'fields': ('risk_level', 'risk_score')
        }),
        ('Distribution', {
            'fields': ('platform_distribution', 'drug_category_distribution')
        }),
        ('Temporal Patterns', {
            'fields': ('activity_timeline',)
        }),
        ('Analysis', {
            'fields': ('analysis_date',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserBehaviorAnalysis)
class UserBehaviorAnalysisAdmin(admin.ModelAdmin):
    """
    Admin for UserBehaviorAnalysis model.
    """
    list_display = [
        'username', 'behavior_type', 'platform', 'risk_score',
        'activity_frequency', 'suspicious_activity_count', 'analysis_start'
    ]
    list_filter = [
        'behavior_type', 'platform', 'risk_score', 'analysis_start'
    ]
    search_fields = ['username', 'user_id', 'platform__name']
    ordering = ['-risk_score', '-created_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user_id', 'username', 'platform', 'behavior_type')
        }),
        ('Behavior Metrics', {
            'fields': ('activity_frequency', 'content_volume', 'interaction_rate')
        }),
        ('Pattern Analysis', {
            'fields': ('posting_schedule', 'content_themes', 'language_patterns')
        }),
        ('Risk Assessment', {
            'fields': ('suspicious_activity_count', 'risk_score')
        }),
        ('Network Analysis', {
            'fields': ('connections_count', 'influence_score')
        }),
        ('Analysis Period', {
            'fields': ('analysis_start', 'analysis_end')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('platform')


@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    """
    Admin for PerformanceMetrics model.
    """
    list_display = [
        'category', 'metric_name', 'current_value', 'target_value',
        'is_healthy', 'performance_score', 'trend', 'recorded_at'
    ]
    list_filter = [
        'category', 'is_healthy', 'trend', 'recorded_at'
    ]
    search_fields = ['metric_name', 'category']
    ordering = ['category', 'metric_name']
    
    fieldsets = (
        ('Metric Info', {
            'fields': ('category', 'metric_name')
        }),
        ('Values', {
            'fields': ('current_value', 'target_value', 'min_value', 'max_value')
        }),
        ('Performance', {
            'fields': ('is_healthy', 'performance_score')
        }),
        ('Thresholds', {
            'fields': ('warning_threshold', 'critical_threshold')
        }),
        ('Analysis', {
            'fields': ('trend', 'historical_values')
        }),
    )
    
    readonly_fields = ['recorded_at', 'updated_at']
    
    actions = ['update_performance_scores']
    
    def update_performance_scores(self, request, queryset):
        """Update performance scores for selected metrics."""
        for metric in queryset:
            metric.update_performance_score()
        updated = queryset.count()
        self.message_user(request, f'{updated} performance scores were updated.')
    update_performance_scores.short_description = "Update performance scores"


@admin.register(AlertMetrics)
class AlertMetricsAdmin(admin.ModelAdmin):
    """
    Admin for AlertMetrics model.
    """
    list_display = [
        'alert_type', 'analysis_date', 'total_alerts', 'acknowledgment_rate',
        'resolution_rate', 'avg_response_time', 'false_positive_rate'
    ]
    list_filter = [
        'alert_type', 'analysis_date'
    ]
    search_fields = ['alert_type']
    ordering = ['-analysis_date', 'alert_type']
    
    fieldsets = (
        ('Alert Info', {
            'fields': ('alert_type', 'analysis_date')
        }),
        ('Alert Counts', {
            'fields': ('total_alerts', 'acknowledged_alerts', 'resolved_alerts', 'escalated_alerts')
        }),
        ('Response Metrics', {
            'fields': ('avg_response_time', 'avg_resolution_time')
        }),
        ('Quality Metrics', {
            'fields': ('false_positive_rate', 'accuracy_rate')
        }),
        ('User Engagement', {
            'fields': ('users_engaged', 'avg_user_response_time')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
