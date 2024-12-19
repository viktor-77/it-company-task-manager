from django.urls import path

from task_manager.views import WorkerListView, index

urlpatterns = [
	path("", index, name="index"),
	path("workers/", WorkerListView.as_view(), name="worker_list"),
]

app_name = "task_manager"
