from django.urls import path

from . import views

app_name="user"
urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('user/<str:username>', views.user_details, name='user')
]
