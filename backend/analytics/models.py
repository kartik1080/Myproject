"""
Analytics models for Hack2Drug system.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from detection.models import Platform, DrugCategory


class AnalyticsReport(models.Model):
    """
    Generated analytics reports.
    """
    REPORT_TYPES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('custom', 'Custom Report'),
    ]
    
    REPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('html', 'HTML'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=REPORT_FORMATS, default='pdf')
    
    # Report details
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict)  # Report parameters and filters
    
    # Generated content
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)  # bytes
    content_summary = models.JSONField(default=dict, blank=True)
    
    # Generation info
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generation_started = models.DateTimeField(auto_now_add=True)
    generation_completed = models.DateTimeField(null=True, blank=True)
    generation_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('generating', 'Generating'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Analytics Report'
        verbose_name_plural = 'Analytics Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
    
    def mark_completed(self, file_path=None, file_size=None, content_summary=None):
        """Mark report generation as completed."""
        self.generation_status = 'completed'
        self.generation_completed = timezone.now()
        if file_path:
            self.file_path = file_path
        if file_size:
            self.file_size = file_size
        if content_summary:
            self.content_summary = content_summary
        self.save(update_fields=[
            'generation_status', 'generation_completed', 'file_path', 
            'file_size', 'content_summary'
        ])
    
    def mark_failed(self):
        """Mark report generation as failed."""
        self.generation_status = 'failed'
        self.save(update_fields=['generation_status'])


class TrendAnalysis(models.Model):
    """
    Trend analysis for various metrics over time.
    """
    METRIC_TYPES = [
        ('detection_rate', 'Detection Rate'),
        ('platform_activity', 'Platform Activity'),
        ('drug_category', 'Drug Category Distribution'),
        ('geographic', 'Geographic Distribution'),
        ('temporal', 'Temporal Patterns'),
        ('user_behavior', 'User Behavior'),
    ]
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    metric_name = models.CharField(max_length=100)
    
    # Time period
    start_date = models.DateField()
    end_date = models.DateField()
    period_type = models.CharField(
        max_length=20,
        choices=[
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ]
    )
    
    # Analysis results
    data_points = models.JSONField(default=list)  # Time series data
    trend_direction = models.CharField(
        max_length=20,
        choices=[
            ('increasing', 'Increasing'),
            ('decreasing', 'Decreasing'),
            ('stable', 'Stable'),
            ('fluctuating', 'Fluctuating'),
        ]
    )
    trend_strength = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    # Statistical measures
    mean_value = models.FloatField()
    median_value = models.FloatField()
    standard_deviation = models.FloatField()
    correlation_coefficient = models.FloatField(null=True, blank=True)
    
    # Insights
    key_insights = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Trend Analysis'
        verbose_name_plural = 'Trend Analyses'
        ordering = ['-end_date', 'metric_type']
        indexes = [
            models.Index(fields=['metric_type', 'start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.metric_name} - {self.start_date} to {self.end_date}"


class GeographicAnalysis(models.Model):
    """
    Geographic analysis of drug-related activities.
    """
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Activity metrics
    total_detections = models.PositiveIntegerField(default=0)
    unique_users = models.PositiveIntegerField(default=0)
    active_channels = models.PositiveIntegerField(default=0)
    
    # Risk assessment
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Risk'),
            ('medium', 'Medium Risk'),
            ('high', 'High Risk'),
            ('critical', 'Critical Risk'),
        ],
        default='low'
    )
    risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    
    # Platform distribution
    platform_distribution = models.JSONField(default=dict, blank=True)
    
    # Drug category distribution
    drug_category_distribution = models.JSONField(default=dict, blank=True)
    
    # Temporal patterns
    activity_timeline = models.JSONField(default=list, blank=True)
    
    # Analysis date
    analysis_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Geographic Analysis'
        verbose_name_plural = 'Geographic Analyses'
        ordering = ['-total_detections', 'country']
        unique_together = ['country', 'region', 'city', 'analysis_date']
    
    def __str__(self):
        location = f"{self.city}, {self.region}" if self.region else self.city
        return f"{location}, {self.country} - {self.total_detections} detections"


class UserBehaviorAnalysis(models.Model):
    """
    Analysis of user behavior patterns.
    """
    BEHAVIOR_TYPES = [
        ('posting_pattern', 'Posting Pattern'),
        ('communication_pattern', 'Communication Pattern'),
        ('content_pattern', 'Content Pattern'),
        ('temporal_pattern', 'Temporal Pattern'),
        ('network_pattern', 'Network Pattern'),
    ]
    
    behavior_type = models.CharField(max_length=30, choices=BEHAVIOR_TYPES)
    
    # User information
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='user_behaviors')
    
    # Behavior metrics
    activity_frequency = models.FloatField(default=0.0)  # activities per day
    content_volume = models.PositiveIntegerField(default=0)
    interaction_rate = models.FloatField(default=0.0)  # interactions per post
    
    # Pattern analysis
    posting_schedule = models.JSONField(default=dict, blank=True)  # time-based patterns
    content_themes = models.JSONField(default=list, blank=True)  # recurring themes
    language_patterns = models.JSONField(default=dict, blank=True)  # language analysis
    
    # Risk indicators
    suspicious_activity_count = models.PositiveIntegerField(default=0)
    risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    
    # Network analysis
    connections_count = models.PositiveIntegerField(default=0)
    influence_score = models.FloatField(default=0.0)
    
    # Analysis period
    analysis_start = models.DateTimeField()
    analysis_end = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Behavior Analysis'
        verbose_name_plural = 'User Behavior Analyses'
        ordering = ['-risk_score', '-created_at']
        indexes = [
            models.Index(fields=['user_id', 'platform', 'behavior_type']),
            models.Index(fields=['risk_score', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_behavior_type_display()} - {self.platform.name}"


class PerformanceMetrics(models.Model):
    """
    System performance metrics.
    """
    METRIC_CATEGORIES = [
        ('system', 'System Performance'),
        ('detection', 'Detection Performance'),
        ('monitoring', 'Monitoring Performance'),
        ('user', 'User Performance'),
        ('security', 'Security Performance'),
    ]
    
    category = models.CharField(max_length=20, choices=METRIC_CATEGORIES)
    metric_name = models.CharField(max_length=100)
    
    # Metric values
    current_value = models.FloatField()
    target_value = models.FloatField(null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    
    # Performance indicators
    is_healthy = models.BooleanField(default=True)
    performance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=1.0
    )
    
    # Historical data
    historical_values = models.JSONField(default=list, blank=True)  # Time series data
    
    # Thresholds
    warning_threshold = models.FloatField(null=True, blank=True)
    critical_threshold = models.FloatField(null=True, blank=True)
    
    # Analysis
    trend = models.CharField(
        max_length=20,
        choices=[
            ('improving', 'Improving'),
            ('stable', 'Stable'),
            ('declining', 'Declining'),
            ('critical', 'Critical'),
        ],
        default='stable'
    )
    
    # Timestamps
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Performance Metric'
        verbose_name_plural = 'Performance Metrics'
        ordering = ['category', 'metric_name']
        unique_together = ['category', 'metric_name', 'recorded_at']
    
    def __str__(self):
        return f"{self.category} - {self.metric_name}: {self.current_value}"
    
    def update_performance_score(self):
        """Update performance score based on current value and thresholds."""
        if self.target_value is not None:
            # Calculate score based on distance from target
            if self.current_value >= self.target_value:
                self.performance_score = 1.0
            else:
                self.performance_score = max(0.0, self.current_value / self.target_value)
        
        # Check thresholds
        if self.critical_threshold and self.current_value >= self.critical_threshold:
            self.is_healthy = False
            self.trend = 'critical'
        elif self.warning_threshold and self.current_value >= self.warning_threshold:
            self.is_healthy = False
            self.trend = 'declining'
        else:
            self.is_healthy = True
        
        self.save(update_fields=['performance_score', 'is_healthy', 'trend'])


class AlertMetrics(models.Model):
    """
    Metrics related to alerts and notifications.
    """
    alert_type = models.CharField(max_length=50)
    
    # Alert counts
    total_alerts = models.PositiveIntegerField(default=0)
    acknowledged_alerts = models.PositiveIntegerField(default=0)
    resolved_alerts = models.PositiveIntegerField(default=0)
    escalated_alerts = models.PositiveIntegerField(default=0)
    
    # Response metrics
    avg_response_time = models.FloatField(default=0.0)  # minutes
    avg_resolution_time = models.FloatField(default=0.0)  # minutes
    
    # Quality metrics
    false_positive_rate = models.FloatField(default=0.0)
    accuracy_rate = models.FloatField(default=0.0)
    
    # User engagement
    users_engaged = models.PositiveIntegerField(default=0)
    avg_user_response_time = models.FloatField(default=0.0)  # minutes
    
    # Analysis period
    analysis_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Alert Metrics'
        verbose_name_plural = 'Alert Metrics'
        ordering = ['-analysis_date', 'alert_type']
        unique_together = ['alert_type', 'analysis_date']
    
    def __str__(self):
        return f"{self.alert_type} - {self.analysis_date}"
    
    @property
    def acknowledgment_rate(self):
        """Calculate acknowledgment rate."""
        if self.total_alerts > 0:
            return (self.acknowledged_alerts / self.total_alerts) * 100
        return 0.0
    
    @property
    def resolution_rate(self):
        """Calculate resolution rate."""
        if self.total_alerts > 0:
            return (self.resolved_alerts / self.total_alerts) * 100
        return 0.0
