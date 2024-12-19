from datetime import date

from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import create_task

TASK_LIST_URL = "task_manager:task_list"


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
