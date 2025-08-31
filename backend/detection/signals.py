"""
Signals for detection app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetectionResult, DetectionPattern, Platform, DetectionAnalytics


@receiver(post_save, sender=DetectionResult)
def update_detection_analytics(sender, instance, created, **kwargs):
    """Update detection analytics when detection result is created/updated."""
    if created:
        # Update platform statistics
        platform = instance.platform
        platform.total_detections += 1
        platform.save()
        
        # Update daily analytics
        from django.utils import timezone
        today = timezone.now().date()
        
        analytics, created = DetectionAnalytics.objects.get_or_create(
            date=today,
            defaults={
                'telegram_detections': 0,
                'instagram_detections': 0,
                'whatsapp_detections': 0,
                'twitter_detections': 0,
                'other_detections': 0,
                'low_severity': 0,
                'medium_severity': 0,
                'high_severity': 0,
                'critical_severity': 0,
                'pending_review': 0,
                'confirmed': 0,
                'false_positives': 0,
                'escalated': 0,
            }
        )
        
        # Update platform-specific counts
        if platform.platform_type == 'telegram':
            analytics.telegram_detections += 1
        elif platform.platform_type == 'instagram':
            analytics.instagram_detections += 1
        elif platform.platform_type == 'whatsapp':
            analytics.whatsapp_detections += 1
        elif platform.platform_type == 'twitter':
            analytics.twitter_detections += 1
        else:
            analytics.other_detections += 1
        
        # Update severity counts
        if instance.severity_level == 'low':
            analytics.low_severity += 1
        elif instance.severity_level == 'medium':
            analytics.medium_severity += 1
        elif instance.severity_level == 'high':
            analytics.high_severity += 1
        elif instance.severity_level == 'critical':
            analytics.critical_severity += 1
        
        # Update status counts
        if instance.status == 'pending':
            analytics.pending_review += 1
        elif instance.status == 'confirmed':
            analytics.confirmed += 1
        elif instance.status == 'false_positive':
            analytics.false_positives += 1
        elif instance.status == 'escalated':
            analytics.escalated += 1
        
        analytics.save()


@receiver(post_save, sender=DetectionPattern)
def update_pattern_usage(sender, instance, **kwargs):
    """Update pattern usage timestamp."""
    from django.utils import timezone
    instance.last_used = timezone.now()
    instance.save(update_fields=['last_used'])


@receiver(post_save, sender=Platform)
def create_platform_connection(sender, instance, created, **kwargs):
    """Create platform connection when platform is created."""
    if created:
        from monitoring.models import PlatformConnection
        PlatformConnection.objects.create(platform=instance)
