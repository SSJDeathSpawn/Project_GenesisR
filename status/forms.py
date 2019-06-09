from django import forms
from .models import Post,Reply

class StatusForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField()

class ReplyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)