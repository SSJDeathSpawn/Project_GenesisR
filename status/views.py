from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from .models import Post,Reply
from userm.models import UserExtended
from .forms import StatusForm,ReplyForm

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

def send(request):
    print(str(request.user))
    if request.method == 'POST':
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
        form = StatusForm()
    context = {
        'form' : form,
        'user' : request.user
    }
    return render(request, 'status/send.html', context)

def user(request, username):
    try:
        user = UserExtended.objects.get(username=username)
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

def replyto(request, no):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(pk=no)
        except(KeyError, Post.DoesNotExist ):
            return HttpResponse("The Post does not exist!")
        if request.method == 'POST':
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
            form = ReplyForm()
    else:
        return HttpResponse("You have to be logged in to perform the action!")
    context = {
        'form': form,
        'post': post,
        'user': request.user
    }
    return render(request, 'status/replyto.html', context=context)
