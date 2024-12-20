from django.test import SimpleTestCase

from task_manager.forms import SearchForm
from task_manager.tests.utils import get_str_over_length_limit


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
