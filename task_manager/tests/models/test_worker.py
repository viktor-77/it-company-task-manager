from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.tests.utils import create_position, create_worker


class WorkerTestCase(TestCase):
	def test_worker_creation_with_position(self) -> None:
		position = create_position()
		user = create_worker(position=position)

		self.assertTrue(get_user_model().objects.filter(pk=user.pk).exists())
		self.assertEqual(user.position, position)

	def test_creation_worker_without_position(self) -> None:
		user = create_worker()

		self.assertTrue(get_user_model().objects.filter(pk=user.pk).exists())
		self.assertIsNone(user.position)

	def test_position_sets_none_on_delete(self) -> None:
		position = create_position()
		user = create_worker(position=position)

		position.delete()
		user.refresh_from_db()

		self.assertTrue(get_user_model().objects.filter(pk=user.pk).exists())
		self.assertIsNone(user.position)

	def test_worker_verbose_names(self) -> None:
		verbose_name = get_user_model()._meta.verbose_name
		verbose_name_plural = get_user_model()._meta.verbose_name_plural

		self.assertEqual(verbose_name, "Worker")
		self.assertEqual(verbose_name_plural, "Workers")

	def test_str_method(self) -> None:
		user = create_worker()
		self.assertEqual(str(user), user.username)
