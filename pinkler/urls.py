from django.contrib import admin
from django.urls import path, include

from .views import landing_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('feed/', include('feed.urls')),
]
