import imp
from multiprocessing import context
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
            
    context = {}
    return render(request, 'base/login_register.html', context)

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains =q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context =  {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    
    return render(request, 'base/home.html',context ) 

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)