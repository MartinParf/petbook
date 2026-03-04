from django.test import TestCase
from django.urls import reverse

class WebHealthCheckTest(TestCase):
    def test_feed_is_online(self):
        # Otestuje, zda hlavní stránka vrací HTTP 200 (OK)
        response = self.client.get(reverse('tweets:feed'))
        self.assertEqual(response.status_code, 200)
