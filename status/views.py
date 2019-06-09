from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from.models import Post,Reply
from .forms import StatusForm

from .models import Post,Reply

def index(request):
    template = loader.get_template('status/index.html')
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    context = {
        'user': user
    }
    print(request.user)
    return HttpResponse(template.render(context, request))

def send(request, user):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                context = {
                    'form' : form,
                    'user' : request.user
                }
                cd = form.cleaned_data
                if cd['title'] != "" and cd['body'] != "":
                    status = Post(user=request.user,title=cd['title'],body=cd['body'],pub_date=timezone.now())
                    status.save()
                    return HttpResponseRedirect(reverse('statmus:index'))
                else:
                    messages.info(request,message="No fields must be empty")
        else:
            form = StatusForm()
    else:
        return HttpResponse("You must be logged in to perform this action!")
    return render(request, 'status/send.html', context)

def verify(request):
    try:
        title = request.POST['title']
        body = request.POST['body']
        username = request.POST['user']
        date = timezone.now()
        try:
            user = User.objects.get(username=username)
        except(KeyError, User.DoesNotExist) :
            return HttpResponse("User does not exist!")
    except :
        return HttpResponse("Something went wrong...")
    else :
        post = Post(title=title, body=body, user=user, pub_date=date)
        post.save()
        return HttpResponseRedirect(reverse('status:index'))

def user(request, username):
    try:
        user = User.objects.get(username=username)
    except(KeyError, User.DoesNotExist):
        return HttpResponse("The user does not exist!")
    else :
        template = loader.get_template('status/user.html')
        context = {
            'user' : user
        }
        return HttpResponse(template.render(context, request))

def details(request, no):
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

def replyto(request, no, username):
    try:
        post = Post.objects.get(pk=no)
        user = User.objects.get(username=username)
    except(KeyError, Post.DoesNotExist, User.DoesNotExist):
        return HttpResponse("The Post or User does not exist!")
    else:
        template = loader.get_template('status/replyto.html')
        context = {
            'post': post,
            'user': user
        }
        return HttpResponse(template.render(context, request))

def verifyr(request):
    try:
        temp = request.POST['reply']
        username = request.POST['username']
        postid = request.POST['postid']
        try:
            user = User.objects.get(username=username)
            post = Post.objects.get(pk=postid)
        except(KeyError, User.DoesNotExist, Post.DoesNotExist) :
            return HttpResponse("User or post does not exist!")
    except :
        return HttpResponse("Something went wrong...")
    else :
        reply = Reply(user=user,text=temp,post=post)
        reply.save()
        return redirect('status:details', no=postid)
