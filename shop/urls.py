from django.urls import path
from . import views

app_name = "shop" 
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<str:category_slug>/', views.product_list, name='list'),
    path('detail/<int:id>/<str:slug>/', views.product_detail, name="detail"),
]