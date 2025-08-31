"""
API models for Hack2Drug system.
"""

from django.db import models
from django.utils import timezone
from users.models import User


class APIAccessLog(models.Model):
    """
    Log of API access and usage.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_access_logs')
    
    # Request details
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.PositiveIntegerField()
    
    # Request data
    request_data = models.JSONField(default=dict, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    
    # Performance metrics
    response_time = models.FloatField()  # milliseconds
    request_size = models.PositiveIntegerField(default=0)  # bytes
    response_size = models.PositiveIntegerField(default=0)  # bytes
    
    # Client information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'API Access Log'
        verbose_name_plural = 'API Access Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp']),
            models.Index(fields=['status_code', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.method} {self.endpoint} - {self.status_code}"


class APIKey(models.Model):
    """
    API keys for external integrations.
    """
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    # Permissions
    permissions = models.JSONField(default=list)  # List of allowed endpoints
    is_active = models.BooleanField(default=True)
    
    # Usage limits
    rate_limit = models.PositiveIntegerField(default=1000)  # requests per hour
    daily_limit = models.PositiveIntegerField(default=10000)  # requests per day
    
    # Statistics
    total_requests = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def is_expired(self):
        """Check if API key is expired."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def can_access_endpoint(self, endpoint):
        """Check if API key can access specific endpoint."""
        if not self.is_active or self.is_expired():
            return False
        
        if not self.permissions:  # No restrictions
            return True
        
        return endpoint in self.permissions
    
    def increment_usage(self):
        """Increment API usage counter."""
        self.total_requests += 1
        self.last_used = timezone.now()
        self.save(update_fields=['total_requests', 'last_used'])


class WebhookEndpoint(models.Model):
    """
    Webhook endpoints for real-time notifications.
    """
    name = models.CharField(max_length=100)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webhook_endpoints')
    
    # Configuration
    events = models.JSONField(default=list)  # List of events to send
    secret = models.CharField(max_length=128)  # Webhook secret for verification
    is_active = models.BooleanField(default=True)
    
    # Delivery settings
    retry_count = models.PositiveIntegerField(default=3)
    timeout = models.PositiveIntegerField(default=30)  # seconds
    
    # Statistics
    total_deliveries = models.PositiveIntegerField(default=0)
    successful_deliveries = models.PositiveIntegerField(default=0)
    failed_deliveries = models.PositiveIntegerField(default=0)
    last_delivery = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Webhook Endpoint'
        verbose_name_plural = 'Webhook Endpoints'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.url}"
    
    @property
    def success_rate(self):
        """Calculate delivery success rate."""
        if self.total_deliveries > 0:
            return (self.successful_deliveries / self.total_deliveries) * 100
        return 0.0


class DataExport(models.Model):
    """
    Data export requests and results.
    """
    EXPORT_FORMATS = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('pdf', 'PDF'),
    ]
    
    EXPORT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_exports')
    
    # Export details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=10, choices=EXPORT_FORMATS)
    
    # Data selection
    model_type = models.CharField(max_length=100)  # e.g., 'detection', 'user'
    filters = models.JSONField(default=dict)  # Export filters
    fields = models.JSONField(default=list)  # Fields to include
    
    # Status and results
    status = models.CharField(max_length=20, choices=EXPORT_STATUS, default='pending')
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    
    # Progress tracking
    total_records = models.PositiveIntegerField(default=0)
    processed_records = models.PositiveIntegerField(default=0)
    progress_percentage = models.FloatField(default=0.0)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Data Export'
        verbose_name_plural = 'Data Exports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_format_display()} - {self.status}"
    
    def start_processing(self):
        """Start the export processing."""
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def update_progress(self, processed, total):
        """Update export progress."""
        self.processed_records = processed
        self.total_records = total
        if total > 0:
            self.progress_percentage = (processed / total) * 100
        self.save(update_fields=['processed_records', 'total_records', 'progress_percentage'])
    
    def mark_completed(self, file_path, file_size):
        """Mark export as completed."""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.file_path = file_path
        self.file_size = file_size
        self.progress_percentage = 100.0
        self.save(update_fields=[
            'status', 'completed_at', 'file_path', 'file_size', 'progress_percentage'
        ])
    
    def mark_failed(self, error_message):
        """Mark export as failed."""
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])


class SystemHealth(models.Model):
    """
    System health monitoring and status.
    """
    COMPONENT_TYPES = [
        ('database', 'Database'),
        ('cache', 'Cache'),
        ('queue', 'Task Queue'),
        ('storage', 'File Storage'),
        ('external_api', 'External API'),
        ('monitoring', 'Monitoring Service'),
        ('ml_service', 'ML Service'),
    ]
    
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('offline', 'Offline'),
    ]
    
    component = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='healthy')
    
    # Health metrics
    response_time = models.FloatField(null=True, blank=True)  # milliseconds
    error_rate = models.FloatField(default=0.0)  # percentage
    availability = models.FloatField(default=100.0)  # percentage
    
    # Details
    details = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    checked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Health'
        verbose_name_plural = 'System Health'
        ordering = ['component']
        unique_together = ['component', 'checked_at']
    
    def __str__(self):
        return f"{self.get_component_display()} - {self.status}"
    
    def update_health(self, status, response_time=None, error_rate=None, availability=None, details=None):
        """Update component health status."""
        self.status = status
        if response_time is not None:
            self.response_time = response_time
        if error_rate is not None:
            self.error_rate = error_rate
        if availability is not None:
            self.availability = availability
        if details is not None:
            self.details = details
        self.updated_at = timezone.now()
        self.save(update_fields=[
            'status', 'response_time', 'error_rate', 'availability', 
            'details', 'updated_at'
        ])
