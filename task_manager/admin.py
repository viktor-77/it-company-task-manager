from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Worker


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
