from django.urls import path

from task_manager.views import (
	index,
	WorkerDeleteView,
	WorkerDetailView,
	WorkerListView,
)

urlpatterns = [
	path("", index, name="index"),
	path("workers/", WorkerListView.as_view(), name="worker_list"),
	path(
		"workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"
	),
	path(
		"workers/delete/<int:pk>/",
		WorkerDeleteView.as_view(),
		name="worker_delete"
	),
]

app_name = "task_manager"
