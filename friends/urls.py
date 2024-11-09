from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('', views.friends_list_view, name='friends_list'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_request'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('search/', views.search_friends, name='search_friends'),
]
