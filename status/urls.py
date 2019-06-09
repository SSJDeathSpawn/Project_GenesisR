from django.urls import path, include
from . import views

app_name = 'status'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:user>', views.send, name='post'),
    path('verify/', views.verify, name='verify'),
    path('users/<str:username>', views.user, name='user'),
    path('details/<int:no>', views.details, name='details'),
    path('replyto/<int:no>/<str:username>',views.replyto, name='replyto'),
    path('verifyr/', views.verifyr, name="verifyr")
]