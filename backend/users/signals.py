"""
Signals for users app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, UserProfile, UserSession, UserActivity


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved."""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    """Log user activity."""
    if created:
        UserActivity.objects.create(
            user=instance,
            activity_type='create',
            description=f'User account created: {instance.username}',
            ip_address='127.0.0.1',  # Default IP for system operations
            resource_type='user',
            resource_id=instance.id
        )


@receiver(post_save, sender=UserSession)
def log_session_activity(sender, instance, created, **kwargs):
    """Log session activity."""
    if created:
        UserActivity.objects.create(
            user=instance.user,
            activity_type='login',
            description=f'User logged in from {instance.ip_address}',
            ip_address=instance.ip_address,
            resource_type='session',
            resource_id=instance.id
        )


@receiver(post_delete, sender=UserSession)
def log_session_end(sender, instance, **kwargs):
    """Log session end."""
    UserActivity.objects.create(
        user=instance.user,
        activity_type='logout',
        description=f'User session ended from {instance.ip_address}',
        ip_address=instance.ip_address,
        resource_type='session',
        resource_id=instance.id
    )
