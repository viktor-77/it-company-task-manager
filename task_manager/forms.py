from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task


class SearchForm(forms.Form):
	query = forms.CharField(
		max_length=100,
		label="",
		widget=forms.TextInput(
			attrs={"placeholder": "Search...", "class": "form-control"}
		)
	)


class TaskForm(forms.ModelForm):
	priority = forms.ChoiceField(
		choices=Task.PRIORITY_CHOICES,
		widget=forms.RadioSelect
	)

	class Meta:
		model = Task
		fields = [
			"name",
			"description",
			"deadline",
			"is_completed",
			"priority",
			"task_type",
			"assignees",
		]
		widgets = {
			"name": forms.TextInput(
				attrs={
					"class": "form-control",
					"placeholder": "Enter task name"
				}
			),
			"description": forms.Textarea(
				attrs={
					"class": "form-control",
					"placeholder": "Enter task description"
				}
			),
			"deadline": forms.DateInput(
				attrs={"class": "form-control", "type": "date"}
			),
			"is_completed": forms.CheckboxInput(
				attrs={"class": "form-check-input"}
			),
			"task_type": forms.RadioSelect(),
			"assignees": forms.SelectMultiple(attrs={"class": "form-select"})
		}


class WorkerBaseForm(forms.ModelForm):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your username",
				"autocomplete": "new-username"
			}
		),
		min_length=5,
	)
	first_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your first name",
			}
		),
		min_length=5,
	)
	last_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your last name",
			}
		),
		min_length=5,
	)
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your email",
			}
		),
	)

	class Meta:
		model = get_user_model()
		fields = (
			"username",
			"first_name",
			"last_name",
			"email",
		)
