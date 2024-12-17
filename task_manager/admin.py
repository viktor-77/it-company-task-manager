from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Task, Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
	list_display = UserAdmin.list_display + ("position",)
	list_editable = ["position"]
	list_filter = ("position",)
	search_fields = ("username", "first_name", "last_name")

	fieldsets = UserAdmin.fieldsets + (
		(("Position", {
			"classes": ("wide", "collapse",),
			"fields": ("position",),
		}),)
	)

	add_fieldsets = UserAdmin.add_fieldsets + (
		(
			(
				"Details",
				{
					"fields": (
						"position",
						"first_name",
						"last_name",
					)
				},
			),
		)
	)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = (
		"name",
		"created_at",
		"deadline",
		"is_completed",
		"priority",
		"task_type",
	)
	list_editable = ["priority", "task_type"]
	list_filter = (
		"created_at",
		"deadline",
		"is_completed",
		"priority",
		"task_type",
		"assignees"
	)
	search_fields = ("name",)
	filter_horizontal = ("assignees",)
