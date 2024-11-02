from django.shortcuts import render


def feedpage_view(request):
    return render(request, 'feed/feed.html')
