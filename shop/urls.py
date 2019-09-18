from django.urls import path
from . import views

app_name = "shop" 
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<str:category_slug>/', views.product_list, name='list'),
    path('detail/<int:id>/<str:slug>/', views.product_detail, name="detail"),
    path('payment/<int:id>/<str:slug>/', views.payment, name="payment"),
    path('success/', views.success, name="success"),
    path('search/', views.search, name='search'),
]