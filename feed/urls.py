from django.urls import path

from .views import bookmark_view, create_post_list, like_unlike_post

app_name = 'feed'

urlpatterns = [
    path('', create_post_list, name='feed'),
    path('liked', like_unlike_post, name='like-post-view'),
    path('bookmark', bookmark_view, name="bookmark-view")
]