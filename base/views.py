from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message
from .forms import RoomForm, RoomCreationForm


def register_view(request):
    page = "register"

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration Successfull!!!")
            return redirect("home")
        else:
            messages.error(request, "Error occured during registration.")

    else:
        form = UserCreationForm()

    context = {"page": page, "form": form}

    return render(request, "base/login_register.html", context)


def login_view(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist.")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "Logout Successfull.")
    return redirect("home")


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q)
    )

    return render(
        request,
        "base/home.html",
        context={
            "rooms": rooms,
            "topics": topics,
            "room_count": room_count,
            "room_messages": room_messages,
        },
    )


def user_profile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'profile' : user, 
        'rooms' : rooms,
        "topics": topics,
        'room_messages' : room_messages
    }
    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by(
        "-created"
    )  # one to many relationship
    participants = room.participants.all()  # many to many relationship

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context=context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomCreationForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        messages.success(request, "Room creation successful!!!.")
        return redirect("home")
    context = {"form": form, 'topics':topics}

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomCreationForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        messages.error(
            request,
            "You are not allowed to update or delete rooms that you do not host.",
        )
        return redirect("home")

    if request.method == "POST":
        form = RoomCreationForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            messages.success(request, "Room update successful!!!.")
            return redirect("home")

    context = {"form": form, 'topics':topics}

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(
            request,
            "You are not allowed to update or delete rooms that you do not host.",
        )
        return redirect("home")

    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deletion successful!!!.")
        return redirect("home")
    context = {
        "obj": room,
    }

    return render(request, "base/delete.html", context)


@login_required(login_url="/login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.error(
            request,
            "You are not allowed to update or delete messages that you did not post.",
        )

    if request.method == "POST":
        message.delete()
        messages.success(request, "Message deletion successful!!!.")
        return redirect("home")
    context = {
        "obj": message,
    }

    return render(request, "base/delete.html", context)
