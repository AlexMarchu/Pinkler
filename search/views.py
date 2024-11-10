from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import PinklerUser
from friends.models import FriendshipRequest

@login_required(login_url='/accounts/login/')
def search_view(request):
    query = request.GET.get('q', '')
    users = PinklerUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
    self_friends = request.user.friends.all()
    self_requested = FriendshipRequest.objects.filter(created_by=request.user, status=FriendshipRequest.SENT).values_list('created_for', flat=True)
    context = {'users': users, 'self_friends': self_friends, 'self_requested': self_requested}
    return render(request, 'search/search.html', context)