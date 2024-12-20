from django.test import SimpleTestCase, TestCase

from task_manager.forms import (
	SearchForm,
	TaskForm,
	WorkerBaseForm,
	WorkerCreateForm,
)
from task_manager.models import Task, Worker
from task_manager.tests.utils import (
	create_position,
	create_task_type,
	create_worker,
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


class WorkerBaseFormTests(TestCase):
	def setUp(self) -> None:
		self.form_data = {
			"username": "test-username",
			"first_name": "first-name",
			"last_name": "last-name",
			"email": "test.user@example.com",
		}

	def test_valid_form(self) -> None:
		form = WorkerBaseForm(data=self.form_data)

		self.assertTrue(form.is_valid())

	def test_required_fields_validation(self) -> None:
		form = WorkerBaseForm(data={})

		self.assertFalse(form.is_valid())
		for field in self.form_data:
			self.assertIn(field, form.errors)

	def test_min_length_name_fields_validation(self) -> None:
		form = WorkerBaseForm(
			data={
				"username": "test",
				"first_name": "test",
				"last_name": "test",
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("username", form.errors)
		self.assertIn("first_name", form.errors)
		self.assertIn("last_name", form.errors)


class WorkerCreateFormTest(TestCase):
	def setUp(self) -> None:
		self.form_data = {
			"username": "test-username",
			"first_name": "first-name",
			"last_name": "last-name",
			"email": "test.user@example.com",
			"position": create_position().pk,
			"password1": "TestPassword123!",
			"password2": "TestPassword123!",
		}

	def test_valid_form(self) -> None:
		form = WorkerCreateForm(data=self.form_data)

		self.assertTrue(form.is_valid())
		worker = form.save()

		self.assertTrue(Worker.objects.filter(pk=worker.pk).exists())

	def test_required_fields(self) -> None:
		form = WorkerCreateForm(data={})

		self.assertFalse(form.is_valid())
		for field in self.form_data:
			self.assertIn(field, form.errors)

	def test_password_mismatch_validation(self) -> None:
		self.form_data["password2"] = self.form_data["password2"][-1]
		form = WorkerCreateForm(data=self.form_data)

		self.assertFalse(form.is_valid())
		self.assertIn("password2", form.errors)

	def test_short_password__validation(self) -> None:
		short_password = "x" * 7
		self.form_data["password1"] = short_password
		self.form_data["password2"] = short_password
		form = WorkerCreateForm(data=self.form_data)

		self.assertFalse(form.is_valid())
		self.assertIn(
			"This password is too short. It must contain at least 8 characters.",
			form.errors["password2"]
		)

	def test_common_password_validation(self) -> None:
		very_common_password = "password"
		self.form_data["password1"] = very_common_password
		self.form_data["password2"] = very_common_password
		form = WorkerCreateForm(data=self.form_data)

		self.assertFalse(form.is_valid())
		self.assertIn("This password is too common.", form.errors["password2"])

	def test_numeric_password__validation(self) -> None:
		numeric_password = "123456789"
		self.form_data["password1"] = numeric_password
		self.form_data["password2"] = numeric_password
		form = WorkerCreateForm(data=self.form_data)

		self.assertFalse(form.is_valid())
		self.assertIn(
			"This password is entirely numeric.", form.errors["password2"]
		)

	def test_similar_attribute_password_validation(self) -> None:
		password_similar_to_username = "test-username"
		self.form_data["password1"] = password_similar_to_username
		self.form_data["password2"] = password_similar_to_username
		form = WorkerCreateForm(data=self.form_data)

		self.assertFalse(form.is_valid())
		self.assertIn(
			"The password is too similar to the username.",
			form.errors["password2"]
		)
