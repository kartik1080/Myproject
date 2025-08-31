"""
Monitoring models for Hack2Drug system.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from detection.models import Platform


class MonitoringSession(models.Model):
    """
    Active monitoring sessions for different platforms.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('stopped', 'Stopped'),
        ('error', 'Error'),
        ('completed', 'Completed'),
    ]
    
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='monitoring_sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitoring_sessions')
    
    # Session details
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Configuration
    target_channels = models.JSONField(default=list)  # List of channels/users to monitor
    keywords = models.JSONField(default=list)  # Keywords to search for
    monitoring_interval = models.PositiveIntegerField(default=300)  # seconds
    max_content_per_session = models.PositiveIntegerField(default=1000)
    
    # Statistics
    content_collected = models.PositiveIntegerField(default=0)
    detections_found = models.PositiveIntegerField(default=0)
    errors_encountered = models.PositiveIntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Monitoring Session'
        verbose_name_plural = 'Monitoring Sessions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.name} - {self.platform.name} ({self.status})"
    
    def start(self):
        """Start the monitoring session."""
        self.status = 'active'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def pause(self):
        """Pause the monitoring session."""
        self.status = 'paused'
        self.save(update_fields=['status'])
    
    def stop(self):
        """Stop the monitoring session."""
        self.status = 'stopped'
        self.ended_at = timezone.now()
        self.save(update_fields=['status', 'ended_at'])
    
    def update_statistics(self, content_count=0, detections=0, errors=0):
        """Update session statistics."""
        self.content_collected += content_count
        self.detections_found += detections
        self.errors_encountered += errors
        self.last_activity = timezone.now()
        self.save(update_fields=[
            'content_collected', 'detections_found', 'errors_encountered', 'last_activity'
        ])


class CollectedContent(models.Model):
    """
    Content collected during monitoring sessions.
    """
    CONTENT_TYPES = [
        ('message', 'Message'),
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('story', 'Story'),
        ('media', 'Media'),
        ('metadata', 'Metadata'),
    ]
    
    monitoring_session = models.ForeignKey(
        MonitoringSession, 
        on_delete=models.CASCADE, 
        related_name='collected_content'
    )
    
    # Content information
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.CharField(max_length=255)  # Platform-specific ID
    content_text = models.TextField(blank=True)
    content_url = models.URLField(blank=True)
    
    # User information
    user_id = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    user_metadata = models.JSONField(default=dict, blank=True)
    
    # Platform information
    channel_id = models.CharField(max_length=255, blank=True)
    channel_name = models.CharField(max_length=255, blank=True)
    
    # Analysis results
    is_suspicious = models.BooleanField(default=False)
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True
    )
    detected_keywords = models.JSONField(default=list, blank=True)
    ml_analysis = models.JSONField(default=dict, blank=True)
    
    # Metadata
    platform_metadata = models.JSONField(default=dict, blank=True)
    location_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField()
    
    # Collection info
    collected_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Collected Content'
        verbose_name_plural = 'Collected Content'
        ordering = ['-collected_at']
        indexes = [
            models.Index(fields=['content_type', 'collected_at']),
            models.Index(fields=['is_suspicious', 'collected_at']),
            models.Index(fields=['monitoring_session', 'collected_at']),
        ]
    
    def __str__(self):
        return f"{self.content_type} from {self.username} - {self.collected_at}"
    
    def mark_suspicious(self, confidence_score, keywords=None, ml_analysis=None):
        """Mark content as suspicious."""
        self.is_suspicious = True
        self.confidence_score = confidence_score
        if keywords:
            self.detected_keywords = keywords
        if ml_analysis:
            self.ml_analysis = ml_analysis
        self.save(update_fields=[
            'is_suspicious', 'confidence_score', 'detected_keywords', 'ml_analysis'
        ])
    
    def mark_processed(self):
        """Mark content as processed."""
        self.processed = True
        self.save(update_fields=['processed'])


class MonitoringRule(models.Model):
    """
    Rules for monitoring and content collection.
    """
    RULE_TYPES = [
        ('keyword_filter', 'Keyword Filter'),
        ('user_filter', 'User Filter'),
        ('channel_filter', 'Channel Filter'),
        ('time_filter', 'Time Filter'),
        ('content_filter', 'Content Filter'),
    ]
    
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    description = models.TextField(blank=True)
    
    # Rule configuration
    conditions = models.JSONField(default=dict)  # JSON conditions
    actions = models.JSONField(default=dict)  # JSON actions
    
    # Settings
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Monitoring Rule'
        verbose_name_plural = 'Monitoring Rules'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"
    
    def should_apply(self, content):
        """Check if rule should apply to given content."""
        # Implementation would check conditions against content
        # This is a placeholder for the actual logic
        return True
    
    def execute(self, content):
        """Execute the rule actions."""
        # Implementation would execute actions based on rule type
        self.last_executed = timezone.now()
        self.save(update_fields=['last_executed'])


class MonitoringMetrics(models.Model):
    """
    Performance metrics for monitoring operations.
    """
    date = models.DateField(unique=True)
    
    # Platform metrics
    telegram_sessions = models.PositiveIntegerField(default=0)
    instagram_sessions = models.PositiveIntegerField(default=0)
    whatsapp_sessions = models.PositiveIntegerField(default=0)
    twitter_sessions = models.PositiveIntegerField(default=0)
    
    # Content metrics
    total_content_collected = models.PositiveIntegerField(default=0)
    suspicious_content_found = models.PositiveIntegerField(default=0)
    false_positives = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    avg_response_time = models.FloatField(default=0.0)  # milliseconds
    success_rate = models.FloatField(default=0.0)  # percentage
    error_rate = models.FloatField(default=0.0)  # percentage
    
    # Resource usage
    cpu_usage = models.FloatField(default=0.0)  # percentage
    memory_usage = models.FloatField(default=0.0)  # percentage
    network_usage = models.FloatField(default=0.0)  # MB
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Monitoring Metrics'
        verbose_name_plural = 'Monitoring Metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Monitoring Metrics for {self.date}"
    
    @property
    def total_sessions(self):
        """Calculate total monitoring sessions."""
        return (self.telegram_sessions + self.instagram_sessions + 
                self.whatsapp_sessions + self.twitter_sessions)
    
    @property
    def detection_rate(self):
        """Calculate detection rate."""
        if self.total_content_collected > 0:
            return (self.suspicious_content_found / self.total_content_collected) * 100
        return 0.0


class PlatformConnection(models.Model):
    """
    Connection status and health for monitored platforms.
    """
    STATUS_CHOICES = [
        ('connected', 'Connected'),
        ('connecting', 'Connecting'),
        ('disconnected', 'Disconnected'),
        ('error', 'Error'),
        ('rate_limited', 'Rate Limited'),
    ]
    
    platform = models.OneToOneField(Platform, on_delete=models.CASCADE, related_name='connection')
    
    # Connection details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disconnected')
    last_connected = models.DateTimeField(null=True, blank=True)
    last_disconnected = models.DateTimeField(null=True, blank=True)
    
    # Health metrics
    response_time = models.FloatField(null=True, blank=True)  # milliseconds
    error_count = models.PositiveIntegerField(default=0)
    rate_limit_remaining = models.PositiveIntegerField(null=True, blank=True)
    rate_limit_reset = models.DateTimeField(null=True, blank=True)
    
    # Connection info
    api_version = models.CharField(max_length=20, blank=True)
    connection_details = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Platform Connection'
        verbose_name_plural = 'Platform Connections'
    
    def __str__(self):
        return f"{self.platform.name} - {self.status}"
    
    def connect(self):
        """Mark platform as connected."""
        self.status = 'connected'
        self.last_connected = timezone.now()
        self.error_count = 0
        self.save(update_fields=['status', 'last_connected', 'error_count'])
    
    def disconnect(self):
        """Mark platform as disconnected."""
        self.status = 'disconnected'
        self.last_disconnected = timezone.now()
        self.save(update_fields=['status', 'last_disconnected'])
    
    def record_error(self):
        """Record a connection error."""
        self.error_count += 1
        if self.error_count >= 5:
            self.status = 'error'
        self.save(update_fields=['error_count', 'status'])
    
    def update_rate_limit(self, remaining, reset_time):
        """Update rate limit information."""
        self.rate_limit_remaining = remaining
        self.rate_limit_reset = reset_time
        if remaining == 0:
            self.status = 'rate_limited'
        self.save(update_fields=['rate_limit_remaining', 'rate_limit_reset', 'status'])
