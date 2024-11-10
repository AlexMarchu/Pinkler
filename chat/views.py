from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/chat_room_vany.html', {'room_name': room_name})


@login_required(login_url='/accounts/login/')
def chats(request):
    return render(request, 'chat/chats.html', {})
