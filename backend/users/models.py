"""
User models for Hack2Drug system.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator


class User(AbstractUser):
    """
    Custom user model with role-based access control.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('analyst', 'Data Analyst'),
        ('investigator', 'Investigator'),
        ('monitor', 'Platform Monitor'),
        ('viewer', 'Viewer'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Approval'),
    ]
    
    # Basic user information
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Professional information
    badge_number = models.CharField(
        max_length=10, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}\d{6}$',
                message='Badge number must be 2 letters followed by 6 digits (e.g., LE123456)'
            )
        ]
    )
    organization = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Security and access
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    # Meta
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_analyst(self):
        return self.role in ['admin', 'analyst']
    
    @property
    def is_investigator(self):
        return self.role in ['admin', 'investigator']
    
    @property
    def is_monitor(self):
        return self.role in ['admin', 'monitor']
    
    def update_last_activity(self):
        """Update last activity timestamp."""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration."""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    
    def unlock_account(self):
        """Unlock account."""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
    
    def increment_failed_login(self):
        """Increment failed login attempts."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal information
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Professional details
    experience_years = models.PositiveIntegerField(default=0)
    specializations = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    
    # Preferences
    notification_preferences = models.JSONField(default=dict, blank=True)
    dashboard_layout = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class UserSession(models.Model):
    """
    Track user sessions and activity.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    
    # Session information
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_info = models.JSONField(default=dict, blank=True)
    
    # Activity tracking
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Security
    is_active = models.BooleanField(default=True)
    is_secure = models.BooleanField(default=False)  # HTTPS connection
    
    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-login_time']
    
    def __str__(self):
        return f"Session {self.session_key} - {self.user.username}"
    
    def end_session(self):
        """End the session."""
        self.logout_time = timezone.now()
        self.is_active = False
        self.save(update_fields=['logout_time', 'is_active'])
    
    @property
    def duration(self):
        """Calculate session duration."""
        end_time = self.logout_time or timezone.now()
        return end_time - self.login_time


class UserActivity(models.Model):
    """
    Track user activities and actions.
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('export', 'Export'),
        ('report', 'Generate Report'),
        ('alert', 'Alert Action'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    
    # Activity details
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    resource_type = models.CharField(max_length=50, blank=True)  # e.g., 'detection', 'user'
    resource_id = models.PositiveIntegerField(null=True, blank=True)
    
    # Context
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'activity_type', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.timestamp}"
