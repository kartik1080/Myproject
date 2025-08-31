"""
Admin configuration for API app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    APIAccessLog, APIKey, WebhookEndpoint, DataExport, SystemHealth
)


@admin.register(APIAccessLog)
class APIAccessLogAdmin(admin.ModelAdmin):
    """
    Admin for APIAccessLog model.
    """
    list_display = [
        'user', 'endpoint', 'method', 'status_code', 'response_time',
        'ip_address', 'timestamp', 'status_display'
    ]
    list_filter = [
        'method', 'status_code', 'timestamp', 'user'
    ]
    search_fields = [
        'user__username', 'user__email', 'endpoint', 'ip_address'
    ]
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Request Info', {
            'fields': ('user', 'endpoint', 'method', 'status_code')
        }),
        ('Request Data', {
            'fields': ('request_data', 'response_data')
        }),
        ('Performance', {
            'fields': ('response_time', 'request_size', 'response_size')
        }),
        ('Client Info', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Timing', {
            'fields': ('timestamp',)
        }),
    )
    
    readonly_fields = ['timestamp']
    
    def status_display(self, obj):
        """Display status with color coding."""
        if obj.status_code < 300:
            color = 'green'
        elif obj.status_code < 400:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            f'<span style="color: {color};">{obj.status_code}</span>'
        )
    status_display.short_description = 'Status'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """
    Admin for APIKey model.
    """
    list_display = [
        'name', 'user', 'is_active', 'rate_limit', 'daily_limit',
        'total_requests', 'last_used', 'expires_at', 'status_display'
    ]
    list_filter = [
        'is_active', 'created_at', 'expires_at'
    ]
    search_fields = [
        'name', 'user__username', 'user__email'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'key', 'user')
        }),
        ('Permissions', {
            'fields': ('permissions',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Usage Limits', {
            'fields': ('rate_limit', 'daily_limit')
        }),
        ('Statistics', {
            'fields': ('total_requests', 'last_used')
        }),
        ('Expiration', {
            'fields': ('expires_at',)
        }),
    )
    
    readonly_fields = [
        'key', 'created_at', 'total_requests', 'last_used'
    ]
    
    actions = ['regenerate_keys', 'deactivate_keys', 'activate_keys']
    
    def status_display(self, obj):
        """Display key status."""
        if obj.is_expired():
            return format_html('<span style="color: red;">● Expired</span>')
        elif not obj.is_active:
            return format_html('<span style="color: gray;">● Inactive</span>')
        else:
            return format_html('<span style="color: green;">● Active</span>')
    status_display.short_description = 'Status'
    
    def regenerate_keys(self, request, queryset):
        """Regenerate API keys."""
        import secrets
        for key in queryset:
            key.key = secrets.token_urlsafe(32)
            key.save()
        updated = queryset.count()
        self.message_user(request, f'{updated} API keys were regenerated.')
    regenerate_keys.short_description = "Regenerate keys"
    
    def deactivate_keys(self, request, queryset):
        """Deactivate selected API keys."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} API keys were deactivated.')
    deactivate_keys.short_description = "Deactivate keys"
    
    def activate_keys(self, request, queryset):
        """Activate selected API keys."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} API keys were activated.')
    activate_keys.short_description = "Activate keys"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    """
    Admin for WebhookEndpoint model.
    """
    list_display = [
        'name', 'url', 'user', 'is_active', 'total_deliveries',
        'success_rate', 'last_delivery', 'status_display'
    ]
    list_filter = [
        'is_active', 'created_at', 'last_delivery'
    ]
    search_fields = [
        'name', 'url', 'user__username'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'url', 'user')
        }),
        ('Configuration', {
            'fields': ('events', 'secret', 'is_active')
        }),
        ('Delivery Settings', {
            'fields': ('retry_count', 'timeout')
        }),
        ('Statistics', {
            'fields': ('total_deliveries', 'successful_deliveries', 'failed_deliveries', 'last_delivery')
        }),
    )
    
    readonly_fields = [
        'created_at', 'updated_at', 'total_deliveries', 'successful_deliveries',
        'failed_deliveries', 'last_delivery'
    ]
    
    actions = ['test_webhooks', 'reset_statistics']
    
    def status_display(self, obj):
        """Display webhook status."""
        if not obj.is_active:
            return format_html('<span style="color: gray;">● Inactive</span>')
        elif obj.success_rate >= 90:
            return format_html('<span style="color: green;">● Excellent</span>')
        elif obj.success_rate >= 70:
            return format_html('<span style="color: orange;">● Good</span>')
        else:
            return format_html('<span style="color: red;">● Poor</span>')
    status_display.short_description = 'Status'
    
    def test_webhooks(self, request, queryset):
        """Test selected webhooks."""
        # This would implement actual webhook testing
        updated = queryset.count()
        self.message_user(request, f'Test initiated for {updated} webhooks.')
    test_webhooks.short_description = "Test webhooks"
    
    def reset_statistics(self, request, queryset):
        """Reset statistics for selected webhooks."""
        for webhook in queryset:
            webhook.total_deliveries = 0
            webhook.successful_deliveries = 0
            webhook.failed_deliveries = 0
            webhook.save()
        updated = queryset.count()
        self.message_user(request, f'Statistics reset for {updated} webhooks.')
    reset_statistics.short_description = "Reset statistics"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(DataExport)
class DataExportAdmin(admin.ModelAdmin):
    """
    Admin for DataExport model.
    """
    list_display = [
        'name', 'user', 'format', 'model_type', 'status', 'progress_percentage',
        'file_size_display', 'created_at'
    ]
    list_filter = [
        'format', 'status', 'model_type', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'user__username'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Export Info', {
            'fields': ('name', 'description', 'user', 'format')
        }),
        ('Data Selection', {
            'fields': ('model_type', 'filters', 'fields')
        }),
        ('Status & Results', {
            'fields': ('status', 'file_path', 'file_size')
        }),
        ('Progress Tracking', {
            'fields': ('total_records', 'processed_records', 'progress_percentage')
        }),
        ('Error Handling', {
            'fields': ('error_message', 'retry_count')
        }),
        ('Timing', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
    )
    
    readonly_fields = [
        'created_at', 'started_at', 'completed_at', 'progress_percentage'
    ]
    
    actions = [
        'retry_exports', 'cancel_exports', 'download_exports'
    ]
    
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
    
    def retry_exports(self, request, queryset):
        """Retry failed exports."""
        failed_exports = queryset.filter(status='failed')
        for export in failed_exports:
            export.status = 'pending'
            export.error_message = ''
            export.retry_count += 1
            export.save()
        updated = failed_exports.count()
        self.message_user(request, f'{updated} failed exports were queued for retry.')
    retry_exports.short_description = "Retry failed exports"
    
    def cancel_exports(self, request, queryset):
        """Cancel pending exports."""
        pending_exports = queryset.filter(status__in=['pending', 'processing'])
        updated = pending_exports.update(status='cancelled')
        self.message_user(request, f'{updated} exports were cancelled.')
    cancel_exports.short_description = "Cancel exports"
    
    def download_exports(self, request, queryset):
        """Download completed exports."""
        completed_exports = queryset.filter(status='completed')
        # This would implement actual file download
        updated = completed_exports.count()
        self.message_user(request, f'Download initiated for {updated} exports.')
    download_exports.short_description = "Download exports"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(SystemHealth)
class SystemHealthAdmin(admin.ModelAdmin):
    """
    Admin for SystemHealth model.
    """
    list_display = [
        'component', 'status', 'response_time', 'error_rate', 'availability',
        'checked_at', 'health_indicator'
    ]
    list_filter = [
        'component', 'status', 'checked_at'
    ]
    search_fields = ['component']
    ordering = ['component', '-checked_at']
    
    fieldsets = (
        ('Component Info', {
            'fields': ('component', 'status')
        }),
        ('Health Metrics', {
            'fields': ('response_time', 'error_rate', 'availability')
        }),
        ('Details', {
            'fields': ('details', 'error_message')
        }),
        ('Timing', {
            'fields': ('checked_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['checked_at', 'updated_at']
    
    actions = ['check_health', 'reset_health']
    
    def health_indicator(self, obj):
        """Display health indicator with color coding."""
        if obj.status == 'healthy':
            if obj.availability >= 99.9:
                color = 'green'
                indicator = '● Excellent'
            elif obj.availability >= 99.0:
                color = 'lightgreen'
                indicator = '● Good'
            else:
                color = 'orange'
                indicator = '● Fair'
        elif obj.status == 'warning':
            color = 'orange'
            indicator = '⚠ Warning'
        elif obj.status == 'critical':
            color = 'red'
            indicator = '✗ Critical'
        else:
            color = 'gray'
            indicator = '○ Offline'
        
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{indicator}</span>'
        )
    health_indicator.short_description = 'Health'
    
    def check_health(self, request, queryset):
        """Check health for selected components."""
        # This would implement actual health checking
        updated = queryset.count()
        self.message_user(request, f'Health check initiated for {updated} components.')
    check_health.short_description = "Check health"
    
    def reset_health(self, request, queryset):
        """Reset health status for selected components."""
        for health in queryset:
            health.status = 'healthy'
            health.error_rate = 0.0
            health.availability = 100.0
            health.error_message = ''
            health.save()
        updated = queryset.count()
        self.message_user(request, f'Health status reset for {updated} components.')
    reset_health.short_description = "Reset health status"
