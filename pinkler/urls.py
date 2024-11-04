from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import landing_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('feed/', include('feed.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
