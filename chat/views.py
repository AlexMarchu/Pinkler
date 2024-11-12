from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Chat

User = get_user_model()


def load_last_50_messages(room_name):
    chat = get_object_or_404(Chat, pk=5)
    return chat.messages.order_by('-timestamp').all()[:50]


def get_chat_id(request, user_id):
    current_user = request.user

    current_user_chats = Chat.objects.filter(participants=current_user)
    chat = current_user_chats.filter(participants__id=user_id).first()

    if chat:
        return JsonResponse({
            'chat_id': chat.pk,
        })
    else:
        new_chat = Chat.objects.create()
        new_chat.participants.add(current_user)
        new_chat.participants.add(get_object_or_404(User, id=user_id))

        return JsonResponse({
            'chat_id': new_chat.pk,
        })


@login_required(login_url='/accounts/login/')
def get_chats(request):
    self_chats = request.user.chats.all()
    chats_and_last_messages = list(
        {
            'username': participant.username,
            'user_id': participant.pk,
            'avatar_url': participant.avatar.url,
            'last_message_content': chat.get_last_message().content if chat.get_last_message() else None,
            'last_message_sender': chat.get_last_message().sender.username if chat.get_last_message() else None,
        } for chat in self_chats for participant in chat.participants.exclude(id=request.user.id)
    )
    print(chats_and_last_messages)
    return JsonResponse(chats_and_last_messages[:5], safe=False)


@login_required(login_url='/accounts/login/')
def chats_view(request):
    self_chats = request.user.chats.all()  # request.user.chats.distinct()
    chats_and_last_messages = list((chat, chat.get_last_message()) for chat in self_chats)
    context = {'self_chats_and_last_messages': chats_and_last_messages}
    return render(request, 'chat/chats.html', context)


@login_required(login_url='/accounts/login/')
def chat_room_view(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    companion = chat.participants.exclude(id=request.user.id)[0]
    context = {'chat_id': chat_id, 'companion': companion}
    return render(request, 'chat/chat_room.html', context)
