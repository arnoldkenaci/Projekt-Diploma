
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthSecurityTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass123')

	def test_profile_requires_login(self):
		response = self.client.get(reverse('profile'))
		self.assertNotEqual(response.status_code, 200)
		self.assertIn(response.status_code, [302, 401, 403])

	def test_login_with_valid_credentials(self):
		response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
		self.assertEqual(response.status_code, 302)  # Should redirect after login

	def test_login_with_invalid_credentials(self):
		response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpass'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Invalid username or password', status_code=200)

	def test_logout_requires_login(self):
		response = self.client.get(reverse('logout'))
		self.assertNotEqual(response.status_code, 200)
		self.assertIn(response.status_code, [302, 401, 403])
