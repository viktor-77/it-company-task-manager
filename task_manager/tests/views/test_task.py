from datetime import date

from django.conf.global_settings import LOGIN_URL
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task
from task_manager.tests.utils import (
	create_task,
	create_task_type,
	create_worker,
	get_actual_deadline,
)

TASK_LIST_URL = "task_manager:task_list"
TASK_CREATE_URL = "task_manager:task_create"
TASK_DETAIL_URL = "task_manager:task_detail"
TASK_UPDATE_URL = "task_manager:task_update"
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


class TaskCreateViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.task_type = create_task_type()
		cls.user = create_worker()
		cls.form_data = {
			"name": "Test Task",
			"description": "Test description",
			"deadline": get_actual_deadline(),
			"is_completed": False,
			"priority": 1,
			"task_type": cls.task_type.pk,
			"assignees": [cls.user.pk]
		}

	def test_task_create_view_login_required(self) -> None:
		response = self.client.post(reverse(TASK_CREATE_URL))

		self.assertEqual(response.status_code, 302)
		self.assertIn(LOGIN_URL, response.url)

	def test_task_create_view_accessible_for_authenticated_users(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse(TASK_CREATE_URL))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_form.html")

	def test_task_create_view_successful_creation(self):
		self.client.force_login(self.user)
		response = self.client.post(
			reverse(TASK_CREATE_URL), data=self.form_data
		)

		self.assertTrue(
			Task.objects.filter(name=self.form_data["name"]).exists()
		)
		created_task = Task.objects.get(name=self.form_data["name"])
		self.assertEqual(
			created_task.description, self.form_data["description"]
		)
		self.assertEqual(created_task.deadline, self.form_data["deadline"])
		self.assertEqual(created_task.is_completed, False)
		self.assertEqual(created_task.priority, self.form_data["priority"])
		self.assertIn(self.user, created_task.assignees.all())
		self.assertRedirects(
			response, reverse(TASK_DETAIL_URL, kwargs={"pk": created_task.pk})
		)

	def test_task_create_view_invalid_form(self):
		self.client.force_login(self.user)
		response = self.client.post(
			reverse(TASK_CREATE_URL), data={}
		)

		self.assertTrue(response.context["form"].errors)


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


class TaskUpdateViewTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.task_type = create_task_type()
		cls.superuser = create_worker(username="admin", is_superuser=True)
		cls.assigned_user = create_worker(username="assigned_user")
		cls.unassigned_user = create_worker(username="unassigned_user")
		cls.task = create_task()
		cls.task.assignees.add(cls.assigned_user)
		cls.form_data = {
			"name": "Updated Task",
			"description": "Updated description",
			"deadline": cls.task.deadline,
			"is_completed": cls.task.is_completed,
			"priority": cls.task.priority,
			"task_type": cls.task.task_type.pk,
			"assignees": [cls.assigned_user.pk]
		}

	def test_task_update_view_not_accessible_for_unauthenticated_users(
		self
	) -> None:
		response = self.client.get(
			reverse(TASK_UPDATE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_task_update_view_not_accessible_for_unassigned_users(self):
		self.client.force_login(self.unassigned_user)
		response = self.client.get(
			reverse(TASK_UPDATE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_task_update_view_accessible_for_assigned_users(self) -> None:
		self.client.force_login(self.assigned_user)
		response = self.client.get(
			reverse(TASK_UPDATE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_form.html")

	def test_task_update_view_accessible_for_superusers(self) -> None:
		self.client.force_login(self.superuser)
		response = self.client.get(
			reverse(TASK_UPDATE_URL, args=[self.task.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/task_form.html")

	def test_task_update_view_successful_update(self):
		self.client.force_login(self.assigned_user)
		response = self.client.post(
			reverse(TASK_UPDATE_URL, args=[self.task.pk]), data=self.form_data
		)
		self.task.refresh_from_db()

		self.assertEqual(self.task.name, self.form_data["name"])
		self.assertTrue(
			Task.objects.filter(name=self.form_data["name"]).exists()
		)
		self.assertRedirects(
			response,
			reverse("task_manager:task_detail", kwargs={"pk": self.task.pk})
		)

	def test_task_update_view_invalid_form(self):
		self.client.force_login(self.assigned_user)
		form_data = self.form_data.copy()
		form_data["name"] = ""
		response = self.client.post(
			reverse(TASK_UPDATE_URL, args=[self.task.pk]), data=form_data
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["form"].errors)
		self.assertIn("name", response.context["form"].errors)


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
