import imp
from multiprocessing import context
from django.shortcuts import render
from .models import Room

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend Developers'},
# ] 


def home(request):
    rooms = Room.objects.all()
    context =  {'rooms': rooms}
    
    return render(request, 'base/home.html',context ) 

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    context = {}
    return render(request, 'base/room_form.html', context)