from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from users.models import PinklerUser
from friends.models import FriendshipRequest


@login_required(login_url='/accounts/login/')
def send_friend_request(request, user_id):
    user_to_add = get_object_or_404(PinklerUser, id=user_id)
    if user_to_add != request.user:
        if FriendshipRequest.objects.filter(created_by=request.user, created_for=user_to_add,
                                            status=FriendshipRequest.SENT).exists():
            return JsonResponse({'error': 'Запрос уже отправлен.'}, status=400)

        FriendshipRequest.objects.create(
            created_by=request.user,
            created_for=user_to_add,
            status=FriendshipRequest.SENT
        )
        return JsonResponse({'success': 'Запрос отправлен!'})
    return JsonResponse({'error': 'Вы не можете отправить запрос себе.'}, status=400)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def accept_friend_request(request, request_id):
    try:
        if request.method != "POST":
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

        friendship_request = get_object_or_404(FriendshipRequest, id=request_id)

        if friendship_request.created_for != request.user:
            return JsonResponse({'error': 'Unauthorized request.'}, status=403)

        if friendship_request.status != FriendshipRequest.SENT:
            return JsonResponse({'error': 'Request already processed.'}, status=400)

        friendship_request.status = FriendshipRequest.ACCEPTED
        friendship_request.save()

        friendship_request.created_by.friends.add(friendship_request.created_for)
        friendship_request.created_for.friends.add(friendship_request.created_by)

        return JsonResponse({'success': 'Запрос принят и вы теперь друзья!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='/accounts/login/')
def remove_friend(request, user_id):
    user_to_remove = get_object_or_404(PinklerUser, id=user_id)
    if request.user.is_friends_with(user_to_remove):
        request.user.remove_friend(user_to_remove)
        return JsonResponse({'success': 'Друг удален.'})
    return JsonResponse({'error': 'Вы не являетесь друзьями с этим пользователем.'}, status=400)

@login_required(login_url='/accounts/login/')
def friends_view(request):
    self_friends = request.user.friends.all()
    self_pending = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT).values_list('created_by', flat=True)
    self_requested = FriendshipRequest.objects.filter(created_by=request.user, status=FriendshipRequest.SENT).values_list('created_for', flat=True)
    context = {'self_friends': self_friends, 'self_requested': self_requested, 'self_pending': self_pending}
    return render(request, 'friends/friends.html', context)