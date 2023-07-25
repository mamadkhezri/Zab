from django import forms

class PostSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)

