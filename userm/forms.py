from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import admin
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'password1', 'password2', 'email')
        model = get_user_model()

class UserChangeFormR(admin.UserChangeForm):
    class Meta:
        fields = '__all__'

class UserCreationFormR(admin.UserCreationForm):
    class Meta:
        fields = '__all__'

class UserAdminR(admin.UserAdmin):
    class Meta:
        fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('username', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser' ),
        }),
        (_('Important dates'), {'fields': ('date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    ) 
    form = UserChangeForm
    add_form = UserSignUpForm
