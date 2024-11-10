from django.urls import path

from .views import feed_view

urlpatterns = [
    path('', feed_view, name='feed'),
]
