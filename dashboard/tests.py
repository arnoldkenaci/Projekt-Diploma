
from django.test import TestCase
from django.urls import reverse

class DashboardSecurityTest(TestCase):
	def test_dashboard_requires_login(self):
		response = self.client.get(reverse('dashboard'))
		self.assertNotEqual(response.status_code, 200)
		self.assertIn(response.status_code, [302, 401, 403])
