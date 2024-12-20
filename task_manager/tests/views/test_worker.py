from datetime import date

from django.conf.global_settings import LOGIN_URL
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import (
	create_position, create_task, create_worker,
)

WORKER_LIST_URL = "task_manager:worker_list"
WORKER_CREATE_URL = "task_manager:worker_create"
WORKER_DETAIL_URL = "task_manager:worker_detail"
WORKER_DELETE_URL = "task_manager:worker_delete"


class WorkerListViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.worker1 = create_worker(
			username="John", first_name="John", last_name="John"
		)
		cls.worker2 = create_worker(
			username="Jane", first_name="Jane", last_name="Jane"
		)

	def test_worker_list_view_is_accessible(self) -> None:
		response = self.client.get(reverse(WORKER_LIST_URL))

		self.assertEqual(response.status_code, 200)

	def test_worker_list_view_template(self) -> None:
		response = self.client.get(reverse(WORKER_LIST_URL))

		self.assertTemplateUsed(response, "pages/worker_list.html")

	def test_worker_list_view_pagination(self) -> None:
		for i in range(10):
			create_worker(username=f"worker{i}")
		response = self.client.get(reverse(WORKER_LIST_URL))

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["is_paginated"])
		self.assertEqual(
			len(response.context["worker_list"]), 10
		)

		response = self.client.get(reverse(WORKER_LIST_URL) + "?page=2")

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["is_paginated"])
		self.assertEqual(
			len(response.context["worker_list"]), 2
		)

	def test_worker_list_view_search_results(self) -> None:
		response = self.client.get(
			reverse(WORKER_LIST_URL) + f"?query={self.worker1.username}"
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.worker1.username)
		self.assertNotContains(response, self.worker2.username)

	def test_worker_list_view_without_search_result(self) -> None:
		response = self.client.get(reverse(WORKER_LIST_URL) + "?query=query")

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context["worker_list"])

	def test_worker_list_view_empty_search_query(self) -> None:
		response = self.client.get(reverse(WORKER_LIST_URL) + "?query=")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			len(response.context["worker_list"]), 2
		)

	def test_worker_list_view_search_form_in_context(self) -> None:
		response = self.client.get(
			reverse(WORKER_LIST_URL) + f"?query={self.worker1.username}"
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn("search_form", response.context)
		self.assertEqual(
			response.context["search_form"].initial["query"],
			self.worker1.username
		)


class WorkerCreateViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = create_worker()
		cls.position = create_position()
		cls.form_data = {
			"username": "test-username",
			"password1": "securepassword123",
			"password2": "securepassword123",
			"first_name": "test-first_name",
			"last_name": "test-last_name",
			"email": "test@email.com",
			"position": cls.position.pk,
		}

	def test_worker_create_view_redirects_authenticated_user_to_index_page(
		self
	):
		self.client.force_login(self.user)
		response = self.client.get(reverse(WORKER_CREATE_URL))

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("task_manager:index"))

	def test_worker_create_view_accessible_for_unauthenticated_users(self):
		response = self.client.get(reverse(WORKER_CREATE_URL))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/worker_form.html")

	def test_worker_create_view_successful_creation(self):
		response = self.client.post(
			reverse(WORKER_CREATE_URL), data=self.form_data
		)

		self.assertTrue(
			get_user_model().objects.filter(
				username=self.form_data["username"]
			).exists()
		)
		user = get_user_model().objects.get(
			username=self.form_data["username"]
		)
		self.assertRedirects(
			response,
			reverse(WORKER_DETAIL_URL, kwargs={"pk": user.pk})
		)
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertEqual(response.wsgi_request.user.pk, user.pk)

	def test_worker_create_view_invalid_form(self):
		self.form_data["password2"] = self.form_data["password2"][-1]
		response = self.client.post(
			reverse(WORKER_CREATE_URL), data=self.form_data
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["form"].errors)
		self.assertIn("password2", response.context["form"].errors)
		self.assertFalse(
			get_user_model().objects.filter(
				username=self.form_data["username"]
			).exists()
		)


class WorkerDetailViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = create_worker()
		cls.active_task1 = create_task(
			name="Active Task 1", is_completed=False
		)
		cls.active_task2 = create_task(
			name="Active Task 2", is_completed=False
		)
		cls.resolved_task1 = create_task(
			name="Resolved Task1", is_completed=True
		)
		cls.resolved_task2 = create_task(
			name="Resolved Task2", is_completed=True
		)

		cls.active_task1.assignees.add(cls.user)
		cls.active_task2.assignees.add(cls.user)
		cls.resolved_task1.assignees.add(cls.user)
		cls.resolved_task2.assignees.add(cls.user)

	def test_worker_detail_view_login_required(self) -> None:
		response = self.client.get(
			reverse(WORKER_DETAIL_URL, args=[self.user.pk])
		)

		self.assertEqual(response.status_code, 302)
		self.assertIn(LOGIN_URL, response.url)

	def test_worker_detail_view_accessible_for_authenticated_users(
		self
	) -> None:
		self.client.force_login(self.user)
		response = self.client.get(
			reverse(WORKER_DETAIL_URL, args=[self.user.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/worker_detail.html")

	def test_worker_detail_view_context_data(self) -> None:
		self.client.force_login(self.user)
		response = self.client.get(
			reverse(WORKER_DETAIL_URL, args=[self.user.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			list(response.context["active_tasks"]),
			[self.active_task1, self.active_task2]
		)
		self.assertEqual(
			list(response.context["resolved_tasks"]),
			[self.resolved_task1, self.resolved_task2]
		)
		self.assertEqual(response.context["today"], date.today())


class WorkerDeleteViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.superuser = create_worker(username="admin", is_superuser=True)
		cls.user = create_worker(username="user")
		cls.test_user = create_worker(username="test-user")

	def test_worker_delete_view_not_accessible_for_unauthenticated_users(
		self
	):
		response = self.client.get(
			reverse(WORKER_DELETE_URL, args=[self.test_user.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_worker_delete_view_not_accessible_for_regular_users(self) -> None:
		self.client.force_login(self.user)
		response = self.client.get(
			reverse(WORKER_DELETE_URL, args=[self.test_user.pk])
		)

		self.assertEqual(response.status_code, 403)

	def test_worker_delete_view_accessible_for_superuser(self) -> None:
		self.client.force_login(self.superuser)
		response = self.client.get(
			reverse(WORKER_DELETE_URL, args=[self.test_user.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/worker_confirm_delete.html")
		self.assertIn("previous_page", response.context)

	def test_worker_delete_successful_for_superuser(self) -> None:
		self.client.force_login(self.superuser)
		response = self.client.post(
			reverse(WORKER_DELETE_URL, args=[self.test_user.pk])
		)

		self.assertFalse(
			get_user_model().objects.filter(pk=self.test_user.pk).exists()
		)
		self.assertRedirects(response, reverse(WORKER_LIST_URL))
