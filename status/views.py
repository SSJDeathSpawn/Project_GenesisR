from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import loader
from django.contrib import messages
from django.utils import timezone
from django.db.models.query import QuerySet
from django.db.models import F, Count
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django import forms
from .models import *
from shop.models import Item
from userm.models import UserExtendedR
from .forms import StatusForm,ReplyForm
from .models import Post,Reply

def index(request):
    if request.method == 'POST':
        if search_handle(request):
            print("Reaching here!")
            return search_handle(request)
    template = loader.get_template('status/index.html')
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    context = {
        'user': user
    }
    return HttpResponse(template.render(context, request))

def search_handle(r):
    if 'searchb' in r.POST:
        text = r.POST['text']
        typ = r.POST['type']
        if text != "": 
            base_url = reverse('status:search')
            query_string = urlencode({'type': typ,'name': text })
            return redirect("{}?{}".format(base_url, query_string))
    return False

@login_required(login_url='/userm/login')
def send(request):
    print(str(request.user))
    if request.method == 'POST':
        if not search_handle(request):
            print("Reached here!")
            form = StatusForm(request.POST)
            if request.user.is_authenticated:
                if form.is_valid():
                    cd = form.cleaned_data
                    if cd['title'] != "" and cd['body'] != "":
                        status = Post(user=request.user,title=cd['title'],body=cd['body'],pub_date=timezone.now())
                        status.save()
                        return HttpResponseRedirect(reverse('status:index'))
                    else:
                        messages.info(request,message="No fields must be empty")
            else:
                return HttpResponse("You must be logged in to perform this action!")
        else:
            return search_handle(request)
    else:
        form = StatusForm()
    context = {
        'form' : form,
        'user' : request.user
    }
    return render(request, 'status/send.html', context)

def user(request, username):
    if request.method == 'POST':
        if search_handle(request):
            return search_handle(request)
    try:
        user = UserExtendedR.objects.get(username=username)
    except(KeyError, UserExtendedR.DoesNotExist):
        return HttpResponse("The user does not exist!")
    else :
        posts = user.post_set.order_by('-pub_date')
        template = loader.get_template('status/user.html')
        context = {
            'user' : user,
            'posts' : posts
        }
        return HttpResponse(template.render(context, request))

def details(request, no):
    if request.method == 'POST':
        if search_handle(request):
            return search_handle(request)
    try:
        post = Post.objects.get(pk=no)
    except(KeyError, Post.DoesNotExist):
        return HttpResponse("The Post does not exist!")
    else:
        template = loader.get_template('status/details.html')
        context = {
            'post': post,
            'user': request.user
        }
        return HttpResponse(template.render(context, request))

@login_required(login_url='/userm/login')
def replyto(request, no):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(pk=no)
        except(KeyError, Post.DoesNotExist ):
            return HttpResponse("The Post does not exist!")
        if request.method == 'POST':
            if not search_handle(request):
                form = ReplyForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    if cd['text'] != "":
                        reply = Reply(user = request.user, text=cd['text'], post=post)
                        reply.save()
                        return redirect('status:details', no=no)
                    else:
                        return HttpResponse("The Text Field cannot be empty")
            else:
                return search_handle(request)
        else:
            form = ReplyForm()
    else:
        return HttpResponse("You have to be logged in to perform the action!")
    context = {
        'form': form,
        'post': post,
        'user': request.user
    }
    return render(request, 'status/replyto.html', context=context)

@login_required(login_url='/userm/login')
def feed(request):
    if request.method == 'POST':
        if search_handle(request):
            return search_handle(request)
    if request.user.is_authenticated:
        lst = Post.objects.none()
        for user in request.user.following.all():
            print(user)
            lst = lst | user.post_set.all()
        lst = lst.distinct().order_by('-pub_date')
        context = {
            'user': request.user,
            'list': lst
        }
        return render(request, 'status/feed.html', context=context)
    else:
        return HttpResponse('You must be logged in to do that!')

@login_required(login_url='/userm/login')
def like(request, id):
    try:
        post = Post.objects.get(pk=id)
    except(KeyError, Post.DoesNotExist):
        return HttpResponse('Post does not exist')
    else:
        if request.user.is_authenticated:
            post.likes += 1
            post.save()
            request.user.post_liked.add(post)
            request.user.save()
        else:
            return HttpResponse('You have to be logged in to do this!')
    return redirect('status:details', id)

@login_required(login_url='/userm/login')
def unlike(request,id):
    try:
        post = Post.objects.get(pk=id)
    except(KeyError, Post.DoesNotExist):
        return HttpResponse('Post does not exist')
    else:
        if request.user.is_authenticated:
            post.likes -= 1
            post.save()
            request.user.post_liked.remove(post)
            request.user.save()
        else:
            return HttpResponse('You have to be logged in to do this!')
    return redirect('status:details', id)

def search(request):
    if request.method == 'POST':
        if search_handle(request):
            return search_handle(request)
    if request.method == 'GET' and 'type' in request.GET and 'name' in request.GET:
        search_type = request.GET.get('type', None)
        search_option = request.GET.get('name', None)
        print(search_type)
        print(search_option)
        if (search_type == '1'):        
            users = UserExtendedR.objects.filter(username__icontains=search_option).annotate(count=Count('user_from_set')).order_by('-count')
            context = {
                'users': users,
                'user': request.user
            }
        elif(search_type == '2'):
            posts = Post.objects.filter(body__icontains=search_option, title__icontains=search_option).order_by('-likes')
            context = {
                'posts': posts,
                'user': request.user 
            }
        elif(search_type == '3'):
            items = Item.objects.filter(name__icontains=search_option)
            context = {
                'items': items,
                'user': request.user
            }
        else:
            return HttpResponseNotFound('This search type does not exist')
    else:
        context = {
            'user': request.user
        }
    return render(request, 'status/search.html', context=context)

def help(request):
    if request.method == 'GET' and 'type' in request.GET and 'name' in request.GET:
        pass

def contact(request):
    if request.method == 'POST':
        if search_handle(request):
            return search_handle(request)
    return render(request, 'status/contact.html')