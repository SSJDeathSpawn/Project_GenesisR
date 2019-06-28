from django import forms
from .models import Post,Reply

class StatusForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

class ReplyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)