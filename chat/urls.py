from django.urls import path
from .views import chats_view, chat_room_view, get_chat_id, get_chats

app_name = 'chat'

urlpatterns = [
    path('', chats_view, name='chats'),
    path('get-chats/', get_chats, name='get_chats'),
    path('<int:chat_id>/', chat_room_view, name='room'),
    path('get-chat-id/<int:user_id>/', get_chat_id, name='get_chat_id'),
]
