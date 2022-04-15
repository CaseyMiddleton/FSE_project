from django import forms

class NameForm(forms.Form):
    first_query = forms.CharField(label='First query:', max_length=245)