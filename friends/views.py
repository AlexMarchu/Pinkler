from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import PinklerUser
from friends.models import FriendshipRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


@login_required
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


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendshipRequest, PinklerUser


@csrf_exempt
@login_required
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


@login_required
def remove_friend(request, user_id):
    user_to_remove = get_object_or_404(PinklerUser, id=user_id)
    if request.user.is_friends_with(user_to_remove):
        request.user.remove_friend(user_to_remove)
        return JsonResponse({'success': 'Друг удален.'})
    return JsonResponse({'error': 'Вы не являетесь друзьями с этим пользователем.'}, status=400)


@login_required
def search_friends(request):
    query = request.GET.get('q', '')
    users = PinklerUser.objects.filter(username__icontains=query).exclude(id=request.user.id)

    # We receive all friendly requests where the current user is the initiator or recipient
    friendship_requests = FriendshipRequest.objects.filter(
        Q(created_by=request.user) | Q(created_for=request.user)
    )

    # We determine which users have already sent requests or are waiting for the request to be accepted
    sent_requests_users = [req.created_for.id for req in friendship_requests if
                           req.created_by == request.user and req.status == FriendshipRequest.SENT]
    received_requests_users = [req.created_by.id for req in friendship_requests if
                               req.created_for == request.user and req.status == FriendshipRequest.SENT]
    received_requests = [req for req in friendship_requests if
                         req.created_for == request.user and req.status == FriendshipRequest.SENT]

    accepted_sent_requests_users = [req.created_for.id for req in friendship_requests if
                                    req.created_by == request.user and req.status == FriendshipRequest.ACCEPTED]
    accepted_received_requests_users = [req.created_by.id for req in friendship_requests if
                                        req.created_for == request.user and req.status == FriendshipRequest.ACCEPTED]

    context = {
        'users': users,
        'sent_requests_users': sent_requests_users,
        'received_requests_users': received_requests_users,
        'received_requests': received_requests,
        'friendship_requests': friendship_requests,
        'accepted_sent_requests': accepted_sent_requests_users,
        'accepted_received_requests': accepted_received_requests_users,
    }

    return render(request, 'friends/friends.html', context)


@login_required
def friends_list_view(request):
    friends = FriendshipRequest.objects.filter(created_for=request.user, status='accepted')

    return render(request, 'friends/friends.html', {'friends': friends})
