from django.urls import path

from .views import feedpage_view

urlpatterns = [
    path('', feedpage_view, name='feed'),
]
