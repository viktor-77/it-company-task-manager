from django.urls import path

from task_manager.views import (
	index,
	WorkerListView,
	WorkerCreateView,
	WorkerDetailView,
	WorkerUpdateView,
	WorkerDeleteView,
	TaskListView,
	TaskCreateView,
	TaskDetailView,
	TaskUpdateView,
	TaskDeleteView,
)

urlpatterns = [
	path("", index, name="index"),
	path("workers/", WorkerListView.as_view(), name="worker_list"),
	path("workers/create/", WorkerCreateView.as_view(), name="worker_create"),
	path(
		"workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"
	),
	path(
		"workers/update/<int:pk>/",
		WorkerUpdateView.as_view(),
		name="worker_update"
	),
	path(
		"workers/delete/<int:pk>/",
		WorkerDeleteView.as_view(),
		name="worker_delete"
	),
	path("tasks/", TaskListView.as_view(), name="task_list"),
	path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
	path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
	path(
		"tasks/update/<int:pk>/", TaskUpdateView.as_view(), name="task_update"
	),
	path(
		"tasks/delete/<int:pk>/", TaskDeleteView.as_view(), name="task_delete"
	),
]

app_name = "task_manager"
