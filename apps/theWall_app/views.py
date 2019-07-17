from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import datetime

def index(request):
    return render(request, 'theWall_app/index.html')

def reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        newUser = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        newUser.save()
    return redirect('/wall')

def log(request):
    errors = User.objects.userValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['first_name'] = user.first_name
    return redirect('/wall')

def wall(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        context = {}
        context['first_name'] = request.session['first_name']
        context['myMessages'] = Message.objects.all()
        print(context['myMessages'])
    return render(request, 'theWall_app/wall.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def createMessage(request):
    if request.method == 'POST':
        newMessage = Message.objects.create(
            content = request.POST['message'],
            user = User.objects.get(id = request.session['user'])
        )
        newMessage.save()
        print('*' * 100)
    return redirect('/wall')

def deleteMessage(request, messageId):
    Message.objects.get(id = messageId).delete()

    return redirect("/wall")

def createComment(request, messageId):
    if request.method == "POST":
        newComment = Comment.objects.create(
            content = request.POST["comment"],
            message = Message.objects.get(id = messageId),
            user = User.objects.get(id = request.session["user"])
        )
        newComment.save()
    return redirect("/wall")