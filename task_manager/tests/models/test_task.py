from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Task
from task_manager.tests.utils import (
	create_task, create_task_type,
	get_actual_deadline,
	get_str_over_length_limit,
	get_past_deadline,
)


class TaskModelTest(TestCase):
	def setUp(self) -> None:
		self.task_type = create_task_type()
		self.task = create_task(
			name="base-test-task", task_type=self.task_type
		)

	def test_name_max_length_validation_on_create(self) -> None:
		with self.assertRaises(ValidationError):
			create_task(name=get_str_over_length_limit())

	def test_name_max_length_validation_on_update(self) -> None:
		self.task.name = get_str_over_length_limit()

		with self.assertRaises(ValidationError):
			self.task.save()

	def test_unique_name_validation_on_create(self) -> None:
		with self.assertRaises(ValidationError):
			create_task(name=self.task.name)

	def test_unique_name_validation_on_update(self) -> None:
		test_task = create_task()
		test_task.name = self.task.name

		with self.assertRaises(ValidationError):
			test_task.save()

	def test_deadline_validation_on_create(self) -> None:
		with self.assertRaises(ValidationError) as context:
			create_task(deadline=get_past_deadline())

		self.assertRaisesMessage(
			context, Task.DEADLINE_ERROR_MESSAGE
		)

	def test_deadline_validation_on_update(self) -> None:
		self.task.deadline = get_past_deadline()

		with self.assertRaises(ValidationError) as context:
			self.task.save()

		self.assertRaisesMessage(
			context, Task.DEADLINE_ERROR_MESSAGE
		)

	def test_is_completed_field_set_false_by_default(self) -> None:
		task = Task.objects.create(
			name="test-name",
			description="description",
			deadline=get_actual_deadline(),
			priority=1,
			task_type=self.task_type,
		)

		self.assertTrue(Task.objects.get(pk=task.pk))
		self.assertFalse(task.is_completed)
