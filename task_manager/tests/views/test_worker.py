from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import (
	create_worker,
)

WORKER_LIST_URL = "task_manager:worker_list"


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
