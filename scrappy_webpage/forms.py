from django import forms

class NameForm(forms.Form):
    first_query = forms.CharField(label='Your name', max_length=245)