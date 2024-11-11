from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Chat


def load_last_50_messages(room_name):
    chat = get_object_or_404(Chat, pk=5)
    # return chat.load_last_50_messages()
    return chat.messages.order_by('-timestamp').all()[:50]


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/chat_room_vany.html', {'room_name': room_name})


@login_required(login_url='/accounts/login/')
def chats_view(request):
    self_chats = request.user.chats.all()  # request.user.chats.distinct()
    chats_and_last_messages = list((chat, chat.get_last_message()) for chat in self_chats)
    context = {'self_chats_and_last_messages': chats_and_last_messages}
    return render(request, 'chat/chats.html', context)


@login_required(login_url='/accounts/login/')
def chat_room_view(request, room_name):
    context = {'room_name': room_name}
    return render(request, 'chat/chat_room.html', context)
