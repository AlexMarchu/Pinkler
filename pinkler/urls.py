from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import landing_view, test, tmp_friends_view, tmp_bookmarks_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('feed/', include('feed.urls')),
    path('chats/', include('chat.urls', namespace='chat')),
    path('test/', test, name='test'),
    path('friends/', tmp_friends_view, name='friends'),
    path('bookmarks/', tmp_bookmarks_view, name='bookmarks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
