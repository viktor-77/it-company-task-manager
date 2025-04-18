from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from task_manager.models import Position, Task


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


class WorkerCreateForm(WorkerBaseForm, UserCreationForm):
	position = forms.ModelChoiceField(
		queryset=Position.objects, widget=forms.RadioSelect,
	)
	password1 = forms.CharField(
		label="Password",
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
				"placeholder": "Enter your password",
				"autocomplete": "new-password",
			}
		),
	)
	password2 = forms.CharField(
		label="Password confirmation",
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
				"placeholder": "Confirm your password",
				"autocomplete": "new-password",
			}
		),
	)

	class Meta(WorkerBaseForm.Meta, UserCreationForm.Meta):
		fields = WorkerBaseForm.Meta.fields + (
			"position", "password1", "password2",
		)


class WorkerUpdateForm(WorkerBaseForm):
	password = forms.CharField(
		label="Password",
		required=False,
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
				"placeholder": "Confirm your password",
				"autocomplete": "new-password",
			}
		),
	)

	class Meta(WorkerBaseForm.Meta):
		fields = WorkerBaseForm.Meta.fields + ("password",)

	def clean_password(self):
		if password := self.cleaned_data.get("password"):
			try:
				validate_password(password, self.instance)
			except ValidationError as error:
				self.add_error("password", error)

		return password
