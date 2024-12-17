from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class WorkerAdminPageTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_superuser(
			username="test-user", password="test-password"
		)

	def setUp(self) -> None:
		self.client.force_login(self.user)

	def test_changelist_page_displays_position(self) -> None:
		url = reverse("admin:task_manager_worker_changelist")
		response = self.client.get(url)

		self.assertContains(response, "position")

	def test_change_page_displays_position(self) -> None:
		url = reverse("admin:task_manager_worker_change", args=[self.user.id])
		response = self.client.get(url)

		self.assertContains(response, "position")

	def test_add_page_displays_position_and_full_name(self) -> None:
		url = reverse("admin:task_manager_worker_add")
		response = self.client.get(url)

		self.assertContains(response, "position")
		self.assertContains(response, "first_name")
		self.assertContains(response, "last_name")
