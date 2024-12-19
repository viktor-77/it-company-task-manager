from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from task_manager.mixins import PreviousPageMixin, SearchMixin
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


class WorkerListView(SearchMixin, ListView):
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


class WorkerDetailView(LoginRequiredMixin, DetailView):
	model = get_user_model()
	context_object_name = "worker"
	template_name = "pages/worker_detail.html"

	queryset = get_user_model().objects.select_related(
		"position"
	).prefetch_related(
		Prefetch(
			"tasks",
			queryset=Task.objects.filter(is_completed=False),
			to_attr="active_tasks"
		),
		Prefetch(
			"tasks",
			queryset=Task.objects.filter(is_completed=True),
			to_attr="resolved_tasks"
		),
	)

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)

		context["active_tasks"] = self.object.active_tasks
		context["resolved_tasks"] = self.object.resolved_tasks
		context["today"] = date.today()

		return context


class WorkerDeleteView(PreviousPageMixin, DeleteView):
	model = get_user_model()
	template_name = "pages/worker_confirm_delete.html"
	success_url = reverse_lazy("task_manager:worker_list")

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			raise PermissionDenied(
				"You are not allowed to delete users."
			)

		return super().dispatch(request, *args, **kwargs)


class TaskListView(SearchMixin, ListView):
	model = Task
	context_object_name = "task_list"
	template_name = "pages/task_list.html"
	paginate_by = 10

	def get_queryset(self):
		queryset = Task.objects.select_related("task_type")
		search_query = str(self.request.GET.get("query", "")).strip()

		if search_query:
			queryset = queryset.filter(name__icontains=search_query)

		return queryset

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context["today"] = date.today()

		return context


class TaskDetailView(LoginRequiredMixin, DetailView):
	model = Task
	context_object_name = "task"
	template_name = "pages/task_detail.html"
	queryset = Task.objects.select_related("task_type").prefetch_related(
		"assignees"
	)

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context["today"] = date.today()
		context["is_assigned"] = self.object.assignees.filter(
			pk=self.request.user.pk
		).exists()

		return context
