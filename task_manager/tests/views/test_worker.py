from datetime import date

from django.conf.global_settings import LOGIN_URL
from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import (
	create_task, create_worker,
)

WORKER_LIST_URL = "task_manager:worker_list"
WORKER_DETAIL_URL = "task_manager:worker_detail"


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
