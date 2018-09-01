from six import iteritems

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.module_loading import import_string


@receiver(user_logged_in)
def logged_expiry_handler(sender, user, request, **kwargs):
    rules = getattr(settings, 'EXPIRY_SESSION_RULES', {})
    for rule_path, expiry in iteritems(rules):
        rule = import_string(rule_path)
        if rule(user, request):
            request.session.set_expiry(expiry)
            break
