from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from task_manager.admin import TaskAdmin, WorkerAdmin
from task_manager.models import Task


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


class WorkerAdminConfigTest(SimpleTestCase):
	def setUp(self) -> None:
		self.admin_instance = WorkerAdmin(get_user_model(), site)

	def test_list_editable_include_position(self) -> None:
		self.assertEqual(self.admin_instance.list_editable, ["position"])

	def test_list_filter_include_position(self) -> None:
		self.assertEqual(self.admin_instance.list_filter, ("position",))

	def test_search_fields_are_correct(self) -> None:
		self.assertEqual(
			self.admin_instance.search_fields,
			("username", "first_name", "last_name")
		)


class TaskAdminConfigTest(SimpleTestCase):
	def setUp(self) -> None:
		self.admin_instance = TaskAdmin(Task, site)

	def test_list_display_is_correct(self) -> None:
		self.assertEqual(
			self.admin_instance.list_display,
			(
				"name",
				"created_at",
				"deadline",
				"is_completed",
				"priority",
				"task_type",
			)
		)

	def test_list_editable_is_correct(self) -> None:
		self.assertEqual(
			self.admin_instance.list_editable, ["priority", "task_type"]
		)

	def test_list_filter_is_correct(self) -> None:
		self.assertEqual(
			self.admin_instance.list_filter,
			(
				"created_at",
				"deadline",
				"is_completed",
				"priority",
				"task_type",
				"assignees"
			)
		)

	def test_search_fields_are_correct(self) -> None:
		self.assertEqual(self.admin_instance.search_fields, ("name",))

	def test_filter_horizontal_is_correct(self) -> None:
		self.assertEqual(self.admin_instance.filter_horizontal, ("assignees",))
