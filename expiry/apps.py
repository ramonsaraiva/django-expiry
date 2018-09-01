from django.apps import AppConfig


class ExpiryConfig(AppConfig):
    name = 'expiry'

    def ready(self):
        import expiry.signals  # noqa
