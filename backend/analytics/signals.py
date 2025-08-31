"""
Signals for analytics app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AnalyticsReport, PerformanceMetrics


@receiver(post_save, sender=AnalyticsReport)
def log_report_generation(sender, instance, created, **kwargs):
    """Log report generation activity."""
    if created:
        from users.models import UserActivity
        UserActivity.objects.create(
            user=instance.generated_by,
            activity_type='report',
            description=f'Generated {instance.report_type} report: {instance.name}',
            ip_address='127.0.0.1',  # Default IP for system operations
            resource_type='analytics_report',
            resource_id=instance.id
        )


@receiver(post_save, sender=PerformanceMetrics)
def update_performance_trends(sender, instance, **kwargs):
    """Update performance trends when metrics are updated."""
    # Add historical value to the list
    if not instance.historical_values:
        instance.historical_values = []
    
    # Keep only last 100 values to prevent excessive growth
    if len(instance.historical_values) >= 100:
        instance.historical_values.pop(0)
    
    instance.historical_values.append({
        'timestamp': instance.recorded_at.isoformat(),
        'value': instance.current_value
    })
    
    # Update trend analysis
    if len(instance.historical_values) > 1:
        values = [v['value'] for v in instance.historical_values]
        if values[-1] > values[-2]:
            instance.trend = 'improving'
        elif values[-1] < values[-2]:
            instance.trend = 'declining'
        else:
            instance.trend = 'stable'
    
    instance.save(update_fields=['historical_values', 'trend'])
