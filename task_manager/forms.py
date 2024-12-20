from django import forms

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
