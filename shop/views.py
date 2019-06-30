from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.core.files import File
from .models import *
from .forms import *

def index(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', context={'user':request.user, 'categories': categories})

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
    form = AddImageForm()
    user = request.user
    categories = Category.objects.all()
    product = get_object_or_404(Item, id=id, slug=slug, available=True)
    if user.is_authenticated and user == product.seller and request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            photo = Photo(photo=cd['image'], item=product)
            photo.save()
    return render(request, 'shop/detail.html', {'product': product, 'user': user, 'categories' : categories, 'form': form})

def add_item(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('You must be logged in to perform this option!')
    form=ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            category = Category.objects.get(name=cd['category'])
            item = Item(name=cd['name'], description=cd['description'], slug=cd['slug'], price=cd['price'], stock=cd['stock'], seller=user, category=category)
            print(type(cd['main_image']))
            photo = Photo(photo=cd['main_image'], item=item)
            item.save()
            photo.save()
            return redirect('shop/list', cd['category'].name)

    return render(request, 'shop/add.html', {'user': user, 'form': form})
