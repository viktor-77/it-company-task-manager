from django.test import TestCase
from django.urls import reverse

from task_manager.tests.utils import create_task, create_worker

INDEX_URL = reverse('task_manager:index')


class IndexViewTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		create_task(name="Task 1", is_completed=False)
		create_task(name="Task 2", is_completed=True)
		create_worker()

	def test_index_view_is_accessible(self) -> None:
		response = self.client.get(INDEX_URL)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "pages/index.html")

	def test_index_view_context_data(self) -> None:
		response = self.client.get(INDEX_URL)

		self.assertEqual(response.context["total_tasks"], 2)
		self.assertEqual(response.context["active_tasks"], 1)
		self.assertEqual(response.context["total_users"], 1)
