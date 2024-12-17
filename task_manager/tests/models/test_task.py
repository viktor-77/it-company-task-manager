from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.tests.utils import (
	create_task, create_task_type,
	get_str_over_length_limit,
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
