from django.test import SimpleTestCase, TestCase

from task_manager.forms import SearchForm, TaskForm
from task_manager.models import Task
from task_manager.tests.utils import (
	create_task_type, create_worker,
	get_actual_deadline,
	get_str_over_length_limit,
)


class FormSearchTest(SimpleTestCase):
	def test_form_with_valid_data(self) -> None:
		search_query = "qwerty"
		form = SearchForm(data={"query": search_query})

		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data["query"], search_query)

	def test_query_max_length_validation(self) -> None:
		form = SearchForm(data={"query": get_str_over_length_limit()})

		self.assertFalse(form.is_valid())
		self.assertIn("query", form.errors)

	def test_query_required_validation(self) -> None:
		form = SearchForm(data={})

		self.assertFalse(form.is_valid())
		self.assertIn("query", form.errors)


class TaskFormTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.task_type = create_task_type()
		cls.worker = create_worker()

	def setUp(self) -> None:
		self.form_data = {
			"name": "Test Task",
			"description": "Test description",
			"deadline": get_actual_deadline(),
			"is_completed": False,
			"priority": 1,
			"task_type": self.task_type.pk,
			"assignees": [self.worker.pk]
		}

	def test_valid_form(self) -> None:
		form = TaskForm(data=self.form_data)

		self.assertTrue(form.is_valid())
		task = form.save()

		self.assertTrue(Task.objects.filter(pk=task.pk).exists())
		self.assertIn(
			self.worker.pk, task.assignees.values_list("pk", flat=True)
		)

	def test_required_fields(self) -> None:
		required_fields = [
			"name",
			"description",
			"deadline",
			"priority",
			"task_type",
			"assignees"
		]
		form = TaskForm(data={})

		self.assertFalse(form.is_valid())
		for field in required_fields:
			self.assertIn(field, form.errors)

	def test_is_completed_not_required_and_is_false_by_default(self) -> None:
		self.form_data.pop("is_completed")
		form = TaskForm(data=self.form_data)

		self.assertTrue(form.is_valid())
		task = form.save()

		self.assertTrue(Task.objects.filter(pk=task.pk).exists())
		self.assertFalse(task.is_completed)
