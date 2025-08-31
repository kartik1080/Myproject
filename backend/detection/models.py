"""
Detection models for Hack2Drug system.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class DrugCategory(models.Model):
    """
    Categories of drugs for classification.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Risk'),
            ('medium', 'Medium Risk'),
            ('high', 'High Risk'),
            ('critical', 'Critical Risk'),
        ],
        default='medium'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Drug Category'
        verbose_name_plural = 'Drug Categories'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_risk_level_display()})"


class DetectionPattern(models.Model):
    """
    Patterns and keywords for drug detection.
    """
    PATTERN_TYPES = [
        ('keyword', 'Keyword Match'),
        ('regex', 'Regular Expression'),
        ('ml_model', 'Machine Learning Model'),
        ('behavioral', 'Behavioral Pattern'),
        ('metadata', 'Metadata Analysis'),
    ]
    
    name = models.CharField(max_length=100)
    pattern_type = models.CharField(max_length=20, choices=PATTERN_TYPES)
    pattern_data = models.TextField()  # JSON or text pattern
    description = models.TextField(blank=True)
    
    # Detection settings
    confidence_threshold = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.7
    )
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1)
    
    # Categories
    drug_categories = models.ManyToManyField(DrugCategory, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Detection Pattern'
        verbose_name_plural = 'Detection Patterns'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_pattern_type_display()})"


class Platform(models.Model):
    """
    Social media platforms being monitored.
    """
    PLATFORM_TYPES = [
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('discord', 'Discord'),
        ('signal', 'Signal'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=20, choices=PLATFORM_TYPES)
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    monitoring_enabled = models.BooleanField(default=True)
    rate_limit = models.PositiveIntegerField(default=100)  # requests per minute
    
    # Statistics
    total_detections = models.PositiveIntegerField(default=0)
    last_monitoring = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"


class DetectionResult(models.Model):
    """
    Results of drug detection analysis.
    """
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('confirmed', 'Confirmed'),
        ('false_positive', 'False Positive'),
        ('escalated', 'Escalated'),
        ('resolved', 'Resolved'),
    ]
    
    # Detection details
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='detections')
    detection_pattern = models.ForeignKey(DetectionPattern, on_delete=models.CASCADE, related_name='results')
    
    # Content information
    content_text = models.TextField()
    content_url = models.URLField(blank=True)
    content_id = models.CharField(max_length=255, blank=True)  # Platform-specific ID
    
    # User information
    user_id = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    user_metadata = models.JSONField(default=dict, blank=True)
    
    # Detection analysis
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    severity_level = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    detected_keywords = models.JSONField(default=list, blank=True)
    ml_predictions = models.JSONField(default=dict, blank=True)
    
    # Status and assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_detections'
    )
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_detections'
    )
    
    # Metadata
    location_data = models.JSONField(default=dict, blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    ip_addresses = models.JSONField(default=list, blank=True)
    
    # Timestamps
    detected_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Detection Result'
        verbose_name_plural = 'Detection Results'
        ordering = ['-detected_at']
        indexes = [
            models.Index(fields=['status', 'severity_level']),
            models.Index(fields=['platform', 'detected_at']),
            models.Index(fields=['assigned_to', 'status']),
        ]
    
    def __str__(self):
        return f"Detection {self.id} - {self.platform.name} - {self.severity_level}"
    
    def assign_to_user(self, user):
        """Assign detection to a user for review."""
        self.assigned_to = user
        self.status = 'pending'
        self.save(update_fields=['assigned_to', 'status'])
    
    def mark_reviewed(self, user, status='reviewed'):
        """Mark detection as reviewed."""
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.status = status
        self.save(update_fields=['reviewed_by', 'reviewed_at', 'status'])
    
    def escalate(self, user):
        """Escalate detection for further investigation."""
        self.status = 'escalated'
        self.assigned_to = user
        self.save(update_fields=['status', 'assigned_to'])


class DetectionAnalytics(models.Model):
    """
    Analytics and statistics for detection results.
    """
    date = models.DateField(unique=True)
    
    # Counts by platform
    telegram_detections = models.PositiveIntegerField(default=0)
    instagram_detections = models.PositiveIntegerField(default=0)
    whatsapp_detections = models.PositiveIntegerField(default=0)
    twitter_detections = models.PositiveIntegerField(default=0)
    other_detections = models.PositiveIntegerField(default=0)
    
    # Counts by severity
    low_severity = models.PositiveIntegerField(default=0)
    medium_severity = models.PositiveIntegerField(default=0)
    high_severity = models.PositiveIntegerField(default=0)
    critical_severity = models.PositiveIntegerField(default=0)
    
    # Counts by status
    pending_review = models.PositiveIntegerField(default=0)
    confirmed = models.PositiveIntegerField(default=0)
    false_positives = models.PositiveIntegerField(default=0)
    escalated = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    avg_confidence_score = models.FloatField(default=0.0)
    detection_rate = models.FloatField(default=0.0)  # detections per hour
    false_positive_rate = models.FloatField(default=0.0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Detection Analytics'
        verbose_name_plural = 'Detection Analytics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
    
    @property
    def total_detections(self):
        """Calculate total detections across all platforms."""
        return (self.telegram_detections + self.instagram_detections + 
                self.whatsapp_detections + self.twitter_detections + 
                self.other_detections)
    
    @property
    def total_by_severity(self):
        """Calculate total detections by severity."""
        return {
            'low': self.low_severity,
            'medium': self.medium_severity,
            'high': self.high_severity,
            'critical': self.critical_severity,
        }


class DetectionRule(models.Model):
    """
    Rules for automatic detection processing.
    """
    RULE_TYPES = [
        ('auto_assign', 'Auto Assignment'),
        ('auto_escalate', 'Auto Escalation'),
        ('notification', 'Notification'),
        ('blocking', 'Content Blocking'),
        ('reporting', 'Auto Reporting'),
    ]
    
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    description = models.TextField(blank=True)
    
    # Conditions
    conditions = models.JSONField(default=dict)  # JSON conditions for rule activation
    
    # Actions
    actions = models.JSONField(default=dict)  # JSON actions to take
    
    # Settings
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Detection Rule'
        verbose_name_plural = 'Detection Rules'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"
    
    def should_trigger(self, detection_result):
        """Check if rule should trigger for given detection."""
        # Implementation would check conditions against detection_result
        # This is a placeholder for the actual logic
        return True
    
    def execute(self, detection_result):
        """Execute the rule actions."""
        # Implementation would execute actions based on rule type
        self.last_executed = timezone.now()
        self.save(update_fields=['last_executed'])
