from django.urls import path
from .views import friends_view, send_friend_request, accept_friend_request, remove_friend, get_request_id, \
    reject_friend_request, cancel_friend_request

app_name = 'friends'

urlpatterns = [
    path('', friends_view, name='friends'),
    path('send-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('remove-friend/<int:user_id>/', remove_friend, name='remove_friend'),
    path('get-request-id/<int:user_id>/', get_request_id, name='get_request_id'),
    path('reject-request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('cancel-request/<int:user_id>/', cancel_friend_request, name='cancel_friend_request'),
]
