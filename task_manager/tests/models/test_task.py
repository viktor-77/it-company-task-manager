import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Task
from task_manager.tests.utils import (
	create_task,
	create_task_type,
	create_worker,
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

	def test_task_type_is_required(self) -> None:
		with self.assertRaises(ValidationError):
			Task.objects.create(
				name="test-name",
				description="description",
				deadline=get_actual_deadline(),
				priority=1,
			)

	def test_task_type_sets_null_on_delete(self) -> None:
		self.task_type.delete()
		self.task.refresh_from_db()

		self.assertTrue(Task.objects.get(pk=self.task.pk))
		self.assertIsNone(self.task.task_type)

	def test_task_assignees_adding(self) -> None:
		user = create_worker()
		self.task.assignees.add(user)

		self.assertIn(user, self.task.assignees.all())

	def test_task_ordering(self) -> None:
		task1 = create_task(
			name="Task 1",
			priority=1,
			deadline=datetime.date(2030, 12, 30)
		)
		task2 = create_task(
			name="Task 2",
			priority=3,
			deadline=datetime.date(2030, 12, 20)
		)
		task3 = create_task(
			name="Task 3",
			priority=3,
			deadline=datetime.date(2030, 12, 10)
		)
		tasks = Task.objects.filter(pk__in=(task1.pk, task2.pk, task3.pk))

		self.assertEqual(list(tasks), [task3, task2, task1])

	def test_str_method(self) -> None:
		self.assertEqual(str(self.task), self.task.name)
