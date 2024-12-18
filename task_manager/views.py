from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
