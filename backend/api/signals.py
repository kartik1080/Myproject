"""
Signals for API app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import APIAccessLog, APIKey, WebhookEndpoint


@receiver(post_save, sender=APIAccessLog)
def update_api_statistics(sender, instance, created, **kwargs):
    """Update API statistics when access log is created."""
    if created:
        # Update API key usage
        if hasattr(instance, 'user') and instance.user:
            # Find API key used for this request
            # This would need to be implemented based on your authentication method
            pass


@receiver(post_save, sender=APIKey)
def log_api_key_creation(sender, instance, created, **kwargs):
    """Log API key creation."""
    if created:
        from users.models import UserActivity
        UserActivity.objects.create(
            user=instance.user,
            activity_type='create',
            description=f'Created API key: {instance.name}',
            ip_address='127.0.0.1',  # Default IP for system operations
            resource_type='api_key',
            resource_id=instance.id
        )


@receiver(post_save, sender=WebhookEndpoint)
def log_webhook_creation(sender, instance, created, **kwargs):
    """Log webhook endpoint creation."""
    if created:
        from users.models import UserActivity
        UserActivity.objects.create(
            user=instance.user,
            activity_type='create',
            description=f'Created webhook endpoint: {instance.name}',
            ip_address='127.0.0.1',  # Default IP for system operations
            resource_type='webhook_endpoint',
            resource_id=instance.id
        )
