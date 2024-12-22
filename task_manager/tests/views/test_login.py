from django.conf.global_settings import LOGIN_URL
from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import create_worker


class LoginViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = create_worker()

	def test_login_view_is_accessible_for_unauthenticated_users(self) -> None:
		response = self.client.get(LOGIN_URL)

		self.assertEqual(response.status_code, 200)

	def test_login_view_is_not_accessible_for_authenticated_users(
		self
	) -> None:
		self.client.force_login(self.user)
		response = self.client.get(LOGIN_URL)

		self.assertRedirects(response, reverse('task_manager:index'))
