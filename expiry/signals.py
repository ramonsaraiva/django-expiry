from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .rules import process_rules


@receiver(user_logged_in)
def logged_expiry_handler(sender, user, request, **kwargs):
    """Processes rules for logged in user."""
    process_rules(request=request, user=user)
