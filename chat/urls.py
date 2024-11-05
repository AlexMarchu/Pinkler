from django.urls import path
from .views import index, room, chats

app_name = 'chat'

urlpatterns = [
    path('', chats, name='chats'),
    path('test/', index, name='index'),
    path('<str:room_name>/', room, name='room'),
]
