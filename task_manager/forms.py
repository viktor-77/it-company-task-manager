from django import forms


class SearchForm(forms.Form):
	query = forms.CharField(
		max_length=100,
		label="",
		widget=forms.TextInput(
			attrs={"placeholder": "Search...", "class": "form-control"}
		)
	)
