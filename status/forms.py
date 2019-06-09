from django import forms

class StatusForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField()