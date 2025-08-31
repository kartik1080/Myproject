"""
Signals for monitoring app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MonitoringSession, CollectedContent, MonitoringMetrics


@receiver(post_save, sender=MonitoringSession)
def update_monitoring_metrics(sender, instance, created, **kwargs):
    """Update monitoring metrics when session is created/updated."""
    if created:
        # Update daily metrics
        from django.utils import timezone
        today = timezone.now().date()
        
        metrics, created = MonitoringMetrics.objects.get_or_create(
            date=today,
            defaults={
                'telegram_sessions': 0,
                'instagram_sessions': 0,
                'whatsapp_sessions': 0,
                'twitter_sessions': 0,
                'total_content_collected': 0,
                'suspicious_content_found': 0,
                'false_positives': 0,
            }
        )
        
        # Update platform-specific session counts
        platform_type = instance.platform.platform_type
        if platform_type == 'telegram':
            metrics.telegram_sessions += 1
        elif platform_type == 'instagram':
            metrics.instagram_sessions += 1
        elif platform_type == 'whatsapp':
            metrics.whatsapp_sessions += 1
        elif platform_type == 'twitter':
            metrics.twitter_sessions += 1
        
        metrics.save()


@receiver(post_save, sender=CollectedContent)
def update_content_metrics(sender, instance, created, **kwargs):
    """Update content metrics when content is collected."""
    if created:
        # Update daily metrics
        from django.utils import timezone
        today = timezone.now().date()
        
        metrics, created = MonitoringMetrics.objects.get_or_create(
            date=today,
            defaults={
                'telegram_sessions': 0,
                'instagram_sessions': 0,
                'whatsapp_sessions': 0,
                'twitter_sessions': 0,
                'total_content_collected': 0,
                'suspicious_content_found': 0,
                'false_positives': 0,
            }
        )
        
        metrics.total_content_collected += 1
        
        if instance.is_suspicious:
            metrics.suspicious_content_found += 1
        
        metrics.save()
        
        # Update session statistics
        session = instance.monitoring_session
        session.content_collected += 1
        if instance.is_suspicious:
            session.detections_found += 1
        session.save()
