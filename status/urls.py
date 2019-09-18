from django.urls import path, include
from . import views

app_name = 'status'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.send, name='post'),
    path('users/<str:username>/', views.user, name='user'),
    path('details/<int:no>/', views.details, name='details'),
    path('replyto/<int:no>/',views.replyto, name='replyto'),
    path('like/<int:id>/', views.like, name='like'),
    path('unlike/<int:id>/', views.unlike, name='unlike'),
    path('contact/', views.contact, name='contact'),
    path('feed/', views.feed, name='feed'),
    path('search/', views.search, name='search'),
    path('help/',views.help, name='help')
]