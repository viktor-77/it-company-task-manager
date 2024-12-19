class PreviousPageMixin:
	"""Adds previous page url to the context."""

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context["previous_page"] = self.request.META.get("HTTP_REFERER", "/")

		return context
