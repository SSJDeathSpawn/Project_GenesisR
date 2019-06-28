from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import admin
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

class UserChangeFormR(admin.UserChangeForm):
    class Meta:
        fields = '__all__'

class UserCreationFormR(admin.UserCreationForm):
    class Meta:
        fields = '__all__'