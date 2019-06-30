from django.shortcuts import render,get_object_or_404
from .models import *

def index(request):
    return render(request, 'shop/index.html', context={'user':request.user})

def product_list(request, category_slug=None):
    category=None
    categories = Category.objects.all()
    products = Item.objects.filter(available=True)
    user= request.user
    if category_slug is not None:
        print(category_slug)
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/list.html', {
        'category': category,
        'categories': categories,
        'products':  products,
        'user': user})

def product_detail(request, id, slug):
    user = request.user
    product = get_object_or_404(Item, id=id, slug=slug, available=True)
    return render(request, 'shop/detail.html', {'product': product, 'user': user})