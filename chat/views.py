from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/chat_room_vany.html', {'room_name': room_name})


def chats(request):
    return render(request, 'chat/chats.html', {})
