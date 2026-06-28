from django.shortcuts import render , redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home (request):
    return render(request, 'home.html')

@login_required
def room(request, room):
    #username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html' , {
        'username' : request.user.username,
        'room' : room,
        'room_details' : room_details
    })


@login_required
def checkview(request):
    room = request.POST['room_name']
   # username = request.POST['username']

    if Room.objects.filter(name = room).exists():
        return redirect('/'+ room + '/')
    else:
        new_room = Room.objects.create(name = room)
        new_room.save()
        return redirect('/'+ room + '/')


@login_required
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value = message, user=request.user.username, room = room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')

@login_required
def getMessages(request,room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room = room_details.id).order_by('date')
    return JsonResponse({"messages" :list(messages.values())})



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Ce pseudo est déjà pris'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Identifiants invalides'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')