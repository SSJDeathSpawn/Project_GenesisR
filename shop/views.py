from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.core.files import File
from django.core.paginator import Paginator
from .models import *
from .forms import *

def index(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', context={'user':request.user, 'categories': categories})

def product_list(request, category_slug=None):
    category=None
    categories = Category.objects.all()
    prod = Item.objects.filter(available=True)
    user= request.user
    if category_slug is not None:
        print(category_slug)
        category = get_object_or_404(Category, slug=category_slug)
        prod = prod.filter(category=category)
        paginator = Paginator(prod, 10)
        page = request.GET.get('page')
        products = paginator.get_page(page)
    return render(request, 'shop/list.html', {
        'category': category,
        'categories': categories,
        'products':  products,
        'user': user})

def product_detail(request, id, slug):
    form = AddImageForm()
    user = request.user
    categories = Category.objects.all()
    product = get_object_or_404(Item, id=id, slug=slug)
    if user.is_authenticated and user == product.seller and request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            photo = Photo(photo=cd['image'], item=product)
            photo.save()
    return render(request, 'shop/detail.html', {'product': product, 'user': user, 'categories' : categories, 'form': form})

def success(request):
    categories = Category.objects.all()
    return render(request, 'shop/success.html', context={'user': request.user, 'categories': categories})

def payment(request, id, slug):
    form = FakePaymentForm()
    user =request.user
    categories = Category.objects.all()
    product = get_object_or_404(Item, id=id, slug=slug)
    if user.is_authenticated:
        if request.method == 'POST':
            form = FakePaymentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                print("Payment succeeded")
                print("Name:", cd['name'])
                print("Address:", cd['address'])
                print("Payment Method:", cd['pay_method'])
                return redirect("shop:success")
    else:
        return HttpResponse('You must be logged in to do that!')

    return render(request, 'shop/payment.html', {'product': product, 'user': user, 'categories': categories, 'form': form})
