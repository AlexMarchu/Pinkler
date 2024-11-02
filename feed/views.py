from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/register/')
def feedpage_view(request):
    return render(request, 'feed/feed.html')
