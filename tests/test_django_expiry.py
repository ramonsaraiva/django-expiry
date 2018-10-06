from unittest.mock import Mock

from django.test import TestCase

from expiry.middleware import ExpirySessionMiddleware

class ExpiryMiddlewareTests(TestCase):

    def setUp(self):
        self.middleware = ExpirySessionMiddleware()
        self.request = Mock()
        self.response = Mock()

    def test_expiry_middleware(self):
        response = self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.request.session.get_expiry_age.call_count, 1)

