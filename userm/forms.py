from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'password1', 'password2', 'email')
        model = get_user_model()
