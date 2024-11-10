from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/chat_room_vany.html', {'room_name': room_name})


@login_required(login_url='/accounts/login/')
def chats(request):
    self_chats = request.user.chats.all() # request.user.chats.distinct()
    context = {'self_chats': self_chats}
    return render(request, 'chat/chats.html', context)
