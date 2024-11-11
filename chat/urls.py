from django.urls import path
from .views import index, room, chats_view, chat_room_view

app_name = 'chat'

urlpatterns = [
    path('', chats_view, name='chats'),
    path('test/', index, name='index'),
    path('<str:room_name>/', chat_room_view, name='room'),
]
