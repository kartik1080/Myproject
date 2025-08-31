"""
Admin configuration for monitoring app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    MonitoringSession, CollectedContent, MonitoringRule, 
    MonitoringMetrics, PlatformConnection
)


@admin.register(MonitoringSession)
class MonitoringSessionAdmin(admin.ModelAdmin):
    """
    Admin for MonitoringSession model.
    """
    list_display = [
        'name', 'platform', 'user', 'status', 'content_collected',
        'detections_found', 'started_at', 'duration_display'
    ]
    list_filter = [
        'status', 'platform', 'started_at', 'last_activity'
    ]
    search_fields = [
        'name', 'description', 'platform__name', 'user__username'
    ]
    ordering = ['-started_at']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('name', 'description', 'platform', 'user')
        }),
        ('Configuration', {
            'fields': ('target_channels', 'keywords', 'monitoring_interval', 'max_content_per_session')
        }),
        ('Statistics', {
            'fields': ('content_collected', 'detections_found', 'errors_encountered')
        }),
        ('Timing', {
            'fields': ('started_at', 'last_activity', 'ended_at')
        }),
    )
    
    readonly_fields = [
        'started_at', 'last_activity', 'ended_at', 'content_collected',
        'detections_found', 'errors_encountered'
    ]
    
    actions = [
        'start_sessions', 'pause_sessions', 'stop_sessions', 'reset_statistics'
    ]
    
    def duration_display(self, obj):
        """Display session duration."""
        if obj.ended_at:
            duration = obj.ended_at - obj.started_at
        else:
            from django.utils import timezone
            duration = timezone.now() - obj.started_at
        
        if duration.days > 0:
            return f"{duration.days}d {duration.seconds // 3600}h"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m"
        else:
            return f"{duration.seconds // 60}m"
    duration_display.short_description = 'Duration'
    
    def start_sessions(self, request, queryset):
        """Start selected monitoring sessions."""
        for session in queryset:
            session.start()
        updated = queryset.count()
        self.message_user(request, f'{updated} monitoring sessions were started.')
    start_sessions.short_description = "Start sessions"
    
    def pause_sessions(self, request, queryset):
        """Pause selected monitoring sessions."""
        for session in queryset:
            session.pause()
        updated = queryset.count()
        self.message_user(request, f'{updated} monitoring sessions were paused.')
    pause_sessions.short_description = "Pause sessions"
    
    def stop_sessions(self, request, queryset):
        """Stop selected monitoring sessions."""
        for session in queryset:
            session.stop()
        updated = queryset.count()
        self.message_user(request, f'{updated} monitoring sessions were stopped.')
    stop_sessions.short_description = "Stop sessions"
    
    def reset_statistics(self, request, queryset):
        """Reset statistics for selected sessions."""
        for session in queryset:
            session.content_collected = 0
            session.detections_found = 0
            session.errors_encountered = 0
            session.save()
        updated = queryset.count()
        self.message_user(request, f'{updated} session statistics were reset.')
    reset_statistics.short_description = "Reset statistics"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('platform', 'user')


@admin.register(CollectedContent)
class CollectedContentAdmin(admin.ModelAdmin):
    """
    Admin for CollectedContent model.
    """
    list_display = [
        'id', 'content_type', 'username', 'channel_name', 'is_suspicious',
        'confidence_score', 'collected_at', 'processed'
    ]
    list_filter = [
        'content_type', 'is_suspicious', 'processed', 'collected_at',
        'monitoring_session__platform'
    ]
    search_fields = [
        'content_text', 'username', 'user_id', 'channel_name', 'content_id'
    ]
    ordering = ['-collected_at']
    
    fieldsets = (
        ('Content Info', {
            'fields': ('content_type', 'content_id', 'content_text', 'content_url')
        }),
        ('User Info', {
            'fields': ('user_id', 'username', 'user_metadata')
        }),
        ('Channel Info', {
            'fields': ('channel_id', 'channel_name')
        }),
        ('Analysis', {
            'fields': ('is_suspicious', 'confidence_score', 'detected_keywords', 'ml_analysis')
        }),
        ('Metadata', {
            'fields': ('platform_metadata', 'location_data', 'timestamp')
        }),
        ('Collection', {
            'fields': ('monitoring_session', 'collected_at', 'processed')
        }),
    )
    
    readonly_fields = ['collected_at']
    
    actions = ['mark_processed', 'mark_suspicious', 'mark_clean']
    
    def mark_processed(self, request, queryset):
        """Mark content as processed."""
        for content in queryset:
            content.mark_processed()
        updated = queryset.count()
        self.message_user(request, f'{updated} content items were marked as processed.')
    mark_processed.short_description = "Mark as processed"
    
    def mark_suspicious(self, request, queryset):
        """Mark content as suspicious."""
        for content in queryset:
            content.mark_suspicious(0.8)  # Default confidence score
        updated = queryset.count()
        self.message_user(request, f'{updated} content items were marked as suspicious.')
    mark_suspicious.short_description = "Mark as suspicious"
    
    def mark_clean(self, request, queryset):
        """Mark content as clean (not suspicious)."""
        updated = queryset.update(is_suspicious=False, confidence_score=None)
        self.message_user(request, f'{updated} content items were marked as clean.')
    mark_clean.short_description = "Mark as clean"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('monitoring_session')


@admin.register(MonitoringRule)
class MonitoringRuleAdmin(admin.ModelAdmin):
    """
    Admin for MonitoringRule model.
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


@admin.register(MonitoringMetrics)
class MonitoringMetricsAdmin(admin.ModelAdmin):
    """
    Admin for MonitoringMetrics model.
    """
    list_display = [
        'date', 'total_sessions', 'total_content_collected', 'suspicious_content_found',
        'success_rate', 'avg_response_time'
    ]
    list_filter = ['date']
    ordering = ['-date']
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Platform Sessions', {
            'fields': (
                'telegram_sessions', 'instagram_sessions', 'whatsapp_sessions', 'twitter_sessions'
            )
        }),
        ('Content Metrics', {
            'fields': (
                'total_content_collected', 'suspicious_content_found', 'false_positives'
            )
        }),
        ('Performance', {
            'fields': (
                'avg_response_time', 'success_rate', 'error_rate'
            )
        }),
        ('Resource Usage', {
            'fields': (
                'cpu_usage', 'memory_usage', 'network_usage'
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PlatformConnection)
class PlatformConnectionAdmin(admin.ModelAdmin):
    """
    Admin for PlatformConnection model.
    """
    list_display = [
        'platform', 'status', 'response_time', 'error_count',
        'rate_limit_remaining', 'last_connected', 'connection_health'
    ]
    list_filter = [
        'status', 'last_connected', 'last_disconnected'
    ]
    search_fields = ['platform__name']
    ordering = ['platform__name']
    
    fieldsets = (
        ('Platform', {
            'fields': ('platform',)
        }),
        ('Connection Status', {
            'fields': ('status', 'last_connected', 'last_disconnected')
        }),
        ('Health Metrics', {
            'fields': ('response_time', 'error_count', 'availability')
        }),
        ('Rate Limiting', {
            'fields': ('rate_limit_remaining', 'rate_limit_reset')
        }),
        ('Connection Details', {
            'fields': ('api_version', 'connection_details')
        }),
    )
    
    readonly_fields = [
        'last_connected', 'last_disconnected', 'created_at', 'updated_at'
    ]
    
    actions = ['test_connection', 'reset_error_count']
    
    def connection_health(self, obj):
        """Display connection health with color coding."""
        if obj.status == 'connected':
            if obj.response_time and obj.response_time < 1000:
                color = 'green'
                health = 'Excellent'
            elif obj.response_time and obj.response_time < 3000:
                color = 'orange'
                health = 'Good'
            else:
                color = 'red'
                health = 'Poor'
        elif obj.status == 'error':
            color = 'red'
            health = 'Error'
        else:
            color = 'gray'
            health = 'Unknown'
        
        return format_html(
            f'<span style="color: {color};">● {health}</span>'
        )
    connection_health.short_description = 'Health'
    
    def test_connection(self, request, queryset):
        """Test connection for selected platforms."""
        # This would implement actual connection testing
        updated = queryset.count()
        self.message_user(request, f'Connection test initiated for {updated} platforms.')
    test_connection.short_description = "Test connection"
    
    def reset_error_count(self, request, queryset):
        """Reset error count for selected connections."""
        updated = queryset.update(error_count=0)
        self.message_user(request, f'Error count reset for {updated} connections.')
    reset_error_count.short_description = "Reset error count"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('platform')
