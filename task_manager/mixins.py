from task_manager.forms import SearchForm


class PreviousPageMixin:
	"""Adds previous page url to the context."""

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context["previous_page"] = self.request.META.get("HTTP_REFERER", "/")

		return context


class SearchMixin:
	"""Adds a search form with the query parameter to the context."""

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		search_query = str(self.request.GET.get("query", "")).strip()

		context["search_form"] = SearchForm(
			initial={"query": search_query}
		)

		return context
