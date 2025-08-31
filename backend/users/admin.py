"""
Admin configuration for users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserSession, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role', 'status',
        'organization', 'badge_number', 'is_active', 'created_at'
    ]
    list_filter = [
        'role', 'status', 'is_active', 'organization', 'created_at',
        'last_login', 'last_activity'
    ]
    search_fields = [
        'username', 'email', 'first_name', 'last_name', 'badge_number',
        'organization', 'department'
    ]
    ordering = ['-created_at']
    
    # Fieldsets for editing
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Info', {
            'fields': ('role', 'organization', 'department', 'badge_number')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Security', {
            'fields': ('last_login_ip', 'failed_login_attempts', 'account_locked_until')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login', 'last_activity')
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'organization'),
        }),
    )
    
    readonly_fields = [
        'last_login', 'date_joined', 'last_activity', 'failed_login_attempts',
        'account_locked_until'
    ]
    
    actions = ['activate_users', 'deactivate_users', 'approve_users', 'suspend_users']
    
    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(status='active', is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(status='inactive', is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def approve_users(self, request, queryset):
        """Approve pending users."""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} users were successfully approved.')
    approve_users.short_description = "Approve selected users"
    
    def suspend_users(self, request, queryset):
        """Suspend selected users."""
        updated = queryset.update(status='suspended', is_active=False)
        self.message_user(request, f'{updated} users were successfully suspended.')
    suspend_users.short_description = "Suspend selected users"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin for UserProfile model.
    """
    list_display = [
        'user', 'experience_years', 'specializations_count', 'certifications_count'
    ]
    list_filter = ['experience_years', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    ordering = ['user__username']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('bio', 'avatar', 'date_of_birth')
        }),
        ('Professional Details', {
            'fields': ('experience_years', 'specializations', 'certifications')
        }),
        ('Preferences', {
            'fields': ('notification_preferences', 'dashboard_layout')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def specializations_count(self, obj):
        """Display count of specializations."""
        return len(obj.specializations) if obj.specializations else 0
    specializations_count.short_description = 'Specializations'
    
    def certifications_count(self, obj):
        """Display count of certifications."""
        return len(obj.certifications) if obj.certifications else 0
    certifications_count.short_description = 'Certifications'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    Admin for UserSession model.
    """
    list_display = [
        'user', 'session_key', 'ip_address', 'login_time', 'last_activity',
        'is_active', 'duration_display'
    ]
    list_filter = [
        'is_active', 'is_secure', 'login_time', 'last_activity'
    ]
    search_fields = [
        'user__username', 'user__email', 'ip_address', 'session_key'
    ]
    ordering = ['-login_time']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'session_key', 'is_active')
        }),
        ('Connection Details', {
            'fields': ('ip_address', 'user_agent', 'device_info', 'is_secure')
        }),
        ('Timing', {
            'fields': ('login_time', 'logout_time', 'last_activity')
        }),
    )
    
    readonly_fields = [
        'login_time', 'last_activity', 'duration_display'
    ]
    
    actions = ['end_sessions']
    
    def duration_display(self, obj):
        """Display session duration in human-readable format."""
        duration = obj.duration
        if duration.days > 0:
            return f"{duration.days}d {duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m"
        else:
            return f"{duration.seconds // 60}m"
    duration_display.short_description = 'Duration'
    
    def end_sessions(self, request, queryset):
        """End selected sessions."""
        for session in queryset:
            session.end_session()
        updated = queryset.count()
        self.message_user(request, f'{updated} sessions were successfully ended.')
    end_sessions.short_description = "End selected sessions"


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin for UserActivity model.
    """
    list_display = [
        'user', 'activity_type', 'resource_type', 'ip_address', 'timestamp'
    ]
    list_filter = [
        'activity_type', 'resource_type', 'timestamp'
    ]
    search_fields = [
        'user__username', 'user__email', 'description', 'ip_address'
    ]
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Activity Info', {
            'fields': ('user', 'activity_type', 'description')
        }),
        ('Resource', {
            'fields': ('resource_type', 'resource_id')
        }),
        ('Context', {
            'fields': ('ip_address', 'user_agent', 'metadata')
        }),
        ('Timing', {
            'fields': ('timestamp',)
        }),
    )
    
    readonly_fields = ['timestamp']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')
