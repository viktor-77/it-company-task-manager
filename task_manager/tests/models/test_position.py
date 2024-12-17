from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Position
from task_manager.tests.utils import (
	create_position,
	get_str_over_length_limit,
)


class PositionTestCase(TestCase):
	def setUp(self) -> None:
		self.position = create_position()

	def test_name_max_length_validation_on_create(self) -> None:
		with self.assertRaises(ValidationError):
			create_position(get_str_over_length_limit())

	def test_name_max_length_validation_on_update(self) -> None:
		self.position.name = get_str_over_length_limit()

		with self.assertRaises(ValidationError):
			self.position.save()

	def test_unique_name_validation_on_create(self) -> None:
		with self.assertRaises(ValidationError):
			create_position(self.position.name)

	def test_unique_name_validation_on_update(self) -> None:
		test_position = create_position("Manager")
		test_position.name = self.position.name

		with self.assertRaises(ValidationError):
			test_position.save()

	def test_ascending_ordering(self) -> None:
		create_position("Manager")
		create_position("Analyst")
		names_list = list(Position.objects.values_list("name", flat=True))

		self.assertEqual(names_list, sorted(names_list))

	def test_str_method(self) -> None:
		self.assertEqual(str(self.position), self.position.name)
