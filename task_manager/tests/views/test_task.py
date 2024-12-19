from datetime import date

from django.conf.global_settings import LOGIN_URL
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task
from task_manager.tests.utils import create_task, create_worker

TASK_LIST_URL = "task_manager:task_list"
TASK_DETAIL_URL = "task_manager:task_detail"
TASK_DELETE_URL = "task_manager:task_delete"


class TaskListViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.task1 = create_task(name="Bug")
		cls.task2 = create_task(name="Fix")

	def test_task_list_view_is_accessible(self) -> None:
		response = self.client.get(reverse(TASK_LIST_URL))

		self.assertEqual(response.status_code, 200)

	def test_task_list_view_template(self) -> None:
		response = self.client.get(reverse(TASK_LIST_URL))

		self.assertTemplateUsed(response, "pages/task_list.html")

	def test_task_list_view_pagination(self) -> None:
		for i in range(10):
			create_task(name=f"test_task{i}")
		response = self.client.get(reverse(TASK_LIST_URL))

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["is_paginated"])
		self.assertEqual(
			len(response.context["task_list"]), 10
		)

		response = self.client.get(reverse(TASK_LIST_URL) + "?page=2")

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["is_paginated"])
		self.assertEqual(
			len(response.context["task_list"]), 2
		)

	def test_task_list_view_search_results(self) -> None:
		response = self.client.get(
			reverse(TASK_LIST_URL) + f"?query={self.task1.name}"
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.task1.name)
		self.assertNotContains(response, self.task2.name)

	def test_task_list_view_search_form_in_context(self) -> None:
		response = self.client.get(
			reverse(TASK_LIST_URL) + f"?query={self.task1.name}"
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn("search_form", response.context)
		self.assertEqual(
			response.context["search_form"].initial["query"], self.task1.name
		)

	def test_task_list_view_without_search_result(self) -> None:
		response = self.client.get(reverse(TASK_LIST_URL) + "?query=query")

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context["task_list"])

	def test_task_list_view_empty_search_query(self) -> None:
		response = self.client.get(reverse(TASK_LIST_URL) + "?query=")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			len(response.context["task_list"]), 2
		)

	def test_task_list_view_today_date_in_context(self) -> None:
		response = self.client.get(reverse(TASK_LIST_URL))

		self.assertEqual(response.context["today"], date.today())


class TaskDetailViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = create_worker()
		cls.unassigned_user = create_worker("unassigned_user")
		cls.task = create_task()
		cls.task.assignees.add(cls.user)

	def test_task_detail_view_login_required(self) -> None:
		response = self.client.get(
			reverse(TASK_DETAIL_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 302)
		self.assertIn(LOGIN_URL, response.url)

	def test_task_detail_view_accessible_for_authenticated_users(self) -> None:
		self.client.force_login(self.user)
		response = self.client.get(
			reverse(TASK_DETAIL_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_detail.html")

	def test_task_detail_view_context_data(self) -> None:
		self.client.force_login(self.user)
		response = self.client.get(
			reverse(TASK_DETAIL_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["today"], date.today())
		self.assertTrue(response.context["is_assigned"])

	def test_task_detail_view_context_data_for_non_assigned_user(self) -> None:
		self.client.force_login(self.unassigned_user)
		response = self.client.get(
			reverse(TASK_DETAIL_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["today"], date.today())
		self.assertFalse(response.context["is_assigned"])


class TaskDeleteViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.superuser = create_worker(username="admin", is_superuser=True)
		cls.unassigned_user = create_worker("user1")
		cls.assigned_user = create_worker("user2")

	def setUp(self) -> None:
		self.task = create_task()
		self.task.assignees.add(self.assigned_user)

	def test_task_delete_view_not_accessible_for_unauthenticated_users(
		self
	) -> None:
		response = self.client.get(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_task_delete_view_not_accessible_for_unassigned_users(
		self
	) -> None:
		self.client.force_login(self.unassigned_user)
		response = self.client.get(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_task_delete_view_accessible_for_assigned_users(self) -> None:
		self.client.force_login(self.assigned_user)
		response = self.client.get(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_confirm_delete.html")
		self.assertIn("previous_page", response.context)

	def test_task_delete_view_accessible_for_superuser(self) -> None:
		self.client.force_login(self.superuser)
		response = self.client.get(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_confirm_delete.html")
		self.assertIn("previous_page", response.context)

	def test_task_delete_successful_for_assigned_user(self) -> None:
		self.client.force_login(self.assigned_user)
		response = self.client.post(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertFalse(
			Task.objects.filter(pk=self.task.pk).exists()
		)
		self.assertRedirects(response, reverse(TASK_LIST_URL))

	def test_task_delete_successful_for_superuser(self) -> None:
		self.client.force_login(self.superuser)
		response = self.client.post(
			reverse(TASK_DELETE_URL, args=[self.task.pk])
		)

		self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
		self.assertRedirects(response, reverse(TASK_LIST_URL))
