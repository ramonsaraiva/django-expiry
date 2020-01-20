from django.conf import settings
from django.utils.module_loading import import_string


def get_settings_key(user):
    return 'AUTH' if user.is_authenticated else 'ANON'


def process_rule(rule, **kwargs):
    """
    Processes a rule. Returns `True` if the rule is valid.

    When the rule is not a callable, tries importing it, assuming it is
    a function defined in a specific module of the application.

    Anonymous rules don't contain an user, so we extract it when calling the
    rule for validation.
    """
    if not callable(rule):
        rule = import_string(rule)

    request = kwargs.pop('request')
    user = kwargs.pop('user', None)
    return rule(request, user) if user.is_authenticated else rule(request)


def process_rules(**kwargs):
    """
    Processes all rules. If a default age is defined, sets the session
    expiry to the default age value.

    Rules will always override the default age.
    """
    request = kwargs.get('request')
    key = get_settings_key(kwargs['user'])

    default_age = getattr(settings, 'EXPIRY_{}_SESSION_AGE'.format(key), None)
    if default_age:
        request.session.set_expiry(default_age)

    rules = getattr(settings, 'EXPIRY_{}_SESSION_RULES'.format(key), ())
    for rule, expiry in rules:
        if process_rule(rule, **kwargs):
            request.session.set_expiry(expiry)
            break
