from django.urls import path

from . import views

app_name="user"
urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('user/<str:username>', views.user_details, name='user'),
    path('edit/', views.edit_user, name='edit'),
    path('logout/', views.logout_user, name='logout'),
    path('friend/<str:user>/<str:user2>', views.friend, name='friend'),
    path('unfriend/<str:user>/<str:user2>', views.unfriend, name='unfriend'),
]
