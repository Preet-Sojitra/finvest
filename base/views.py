from ast import If
import imp
from multiprocessing import context
from pydoc import pager
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm
import requests

request_url = "https://newsapi.org/v2/top-headlines?q=startup&apiKey=573bf6d9bf2c451eb2caf5a1715cf522"
news = {}

def call_news(i):
    data = requests.get(url=request_url)
    js1 = data.json()
    return js1['articles'][i]['description'], js1['articles'][i]['title'], js1['articles'][i]['url']


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
           
            user =  form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        messages.error(request, 'An error occur during registration')
    
    return render(request, 'base/login_register.html', {'form': form})


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
    
    
    for i in range(5):
        description, title, url = call_news(i)
        news[title] = [description, url]
        

    context =  {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'news':news}
    
    return render(request, 'base/home.html',context ) 

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics_segment.html', {'topics': topics})



def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {'room': room}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()

    for i in range(5):
        description, title, url = call_news(i)
        news[title] = [description, url]

    context = {'user': user, 'rooms': rooms, 'topics': topics, 'news':news}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)