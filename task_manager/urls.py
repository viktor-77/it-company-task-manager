from django.urls import path

from task_manager.views import (
	index,
	WorkerDetailView,
	WorkerListView,
)

urlpatterns = [
	path("", index, name="index"),
	path("workers/", WorkerListView.as_view(), name="worker_list"),
	path(
		"workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"
	),
]

app_name = "task_manager"
