from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import home_view, tmp_bookmarks_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('feed/', include('feed.urls')),
    path('chats/', include('chat.urls', namespace='chat')),
    path('friends/', include('friends.urls', namespace='friends')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)