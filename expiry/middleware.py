from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    class MiddlewareMixin:
        pass

from .rules import (
    get_settings_key,
    process_rules,
)


class ExpirySessionMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """
        If the current session is fresh (was just created by the default
        session middleware, setting its expiry to `SESSION_COOKIE_AGE`)
        or the session is configured to keep alive, processes all rules
        to identify what `expiry` should be set.
        """
        if not (hasattr(request, 'user') and hasattr(request, 'session')):
            return response

        key = get_settings_key(request.user)

        fresh_session = (
            request.session.get_expiry_age() == settings.SESSION_COOKIE_AGE
        )
        keep_alive = getattr(
            settings, 'EXPIRY_{}_KEEP_ALIVE'.format(key), False
        )

        if fresh_session or keep_alive:
            process_rules(request=request, user=request.user)

        return response
