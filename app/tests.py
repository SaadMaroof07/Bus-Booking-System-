from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from app.models import CustomUser


@override_settings(DEBUG=True, SECURE_SSL_REDIRECT=False)
class SignUpSecurityTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_anonymous_users_can_only_create_accounts(self):
		response = self.client.get('/signup/')

		self.assertEqual(response.status_code, 401)

	def test_signup_ignores_privileged_account_fields(self):
		response = self.client.post(
			'/signup/',
			{
				'username': 'new_customer',
				'password': 'SafePass123!',
				'email': 'customer@example.com',
				'role': 'SA',
				'is_staff': True,
				'is_active': False,
			},
			format='json',
		)

		user = CustomUser.objects.get(username='new_customer')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(user.role, 'C')
		self.assertFalse(user.is_staff)
		self.assertTrue(user.is_active)
		self.assertTrue(user.check_password('SafePass123!'))

	def test_superuser_can_list_accounts(self):
		superuser = CustomUser.objects.create_superuser(
			username='admin', password='SafePass123!', email='admin@example.com'
		)
		self.client.force_authenticate(user=superuser)

		response = self.client.get('/signup/')

		self.assertEqual(response.status_code, 200)
