from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView

from task_manager.models import Task


def index(request: HttpRequest) -> HttpResponse:
	task_counts = Task.objects.aggregate(
		total_tasks=Count("id"),
		active_tasks=Count("id", filter=Q(is_completed=False))
	)

	return render(
		request,
		"pages/index.html",
		{
			"total_tasks": task_counts["total_tasks"],
			"active_tasks": task_counts["active_tasks"],
			"total_users": get_user_model().objects.count(),
		}
	)


class LoginView(BaseLoginView):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("task_manager:index")

		return super().dispatch(request, *args, **kwargs)


class WorkerListView(ListView):
	model = get_user_model()
	context_object_name = "worker_list"
	template_name = "pages/worker_list.html"
	paginate_by = 10

	def get_queryset(self):
		queryset = get_user_model().objects.select_related("position")
		search_query = str(self.request.GET.get("query", "")).strip()

		if search_query:
			queryset = queryset.filter(
				Q(username__icontains=search_query) |
				Q(first_name__icontains=search_query) |
				Q(last_name__icontains=search_query)
			)

		return queryset
