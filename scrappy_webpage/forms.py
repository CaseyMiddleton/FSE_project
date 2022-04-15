from email.policy import default
from django import forms
from scrappy_webpage.choices import *

class NameForm(forms.Form):
    first_query = forms.CharField(label='First query:', max_length=245)
    connector = forms.ChoiceField(label='', choices = CONNECTOR_CHOICES,widget=forms.Select(), required=False)
    second_query = forms.CharField(label='Second query:', max_length=245, required=False)