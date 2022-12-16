from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm as UserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required #to restrict pages from no users
# from django.contrib.auth.forms import UserCreationForm # to get the form to crate a new user

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    context = {'page' : page}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist!')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Password does not match')
    return render(request, 'base/login_registration.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')
    
def registerPage(request):
    form = UserCreationForm()
    page = 'register'
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False) # we want to freeze the process to sava the user name as lower case in all
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')      
        else:
             messages.error(request,'An error occurred during the registration!')
    return render(request, 'base/signup.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.all()[0:4]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))#.order_by('-created')
    rooms = Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q)| Q(description__icontains=q))
    context = {'rooms': rooms,'topics': topics, 'room_count': rooms.count(),'room_messages': room_messages }
    return render(request, 'base/home.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms': rooms,'room_messages':room_messages,'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    context = {'user': user,'form':form}
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES ,instance=user,)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    return render(request, 'base/edit-user.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # here we are quarrying into the messages table where room name is the same and ordering in descending order so that we can see the last comment in first 
    participants = room.participants.all()
    # print('participants - ',participants)
    if request.method == 'POST':
        message = Message.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id )
    context = {'room': room,'room_messages': room_messages,'participants' : participants}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    # print("request . method",request.method)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name= request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form' : RoomForm(),'topics': topics, 'status': 'create'}
    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    context ={'form': form,'topics':topics,'room':room, 'status': 'update'}
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    context = {'obj': room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)
   
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)
    context = {'obj': message}
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {'topics': topics}
    return render(request,'base/topics.html', context)

