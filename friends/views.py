from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from users.models import PinklerUser
from friends.models import FriendshipRequest





@csrf_exempt
@login_required(login_url='/accounts/login/')
def get_request_id(request, user_id):
    try:
        friendship_request = FriendshipRequest.objects.get(
            created_for=request.user, created_by_id=user_id, status=FriendshipRequest.SENT
        )
        return JsonResponse({'request_id': friendship_request.id})
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'error': 'Запрос не найден'}, status=404)



@csrf_exempt
@login_required(login_url='/accounts/login/')
def send_friend_request(request, user_id):
    user_to_send_request = get_object_or_404(PinklerUser, id=user_id)

    existing_request = FriendshipRequest.objects.filter(
        created_by=request.user,
        created_for=user_to_send_request,
        status=FriendshipRequest.SENT
    ).first()

    if existing_request:
        return JsonResponse({'error': 'Запрос уже отправлен'})

    FriendshipRequest.objects.create(
        created_for=user_to_send_request,
        created_by=request.user,
        status=FriendshipRequest.SENT
    )

    return JsonResponse({'success': 'Запрос отправлен!'})


@csrf_exempt
@login_required(login_url='/accounts/login/')
def accept_friend_request(request, request_id):
    try:
        if request.method != "POST":
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

        friendship_request = get_object_or_404(FriendshipRequest, id=request_id)

        if friendship_request.created_for != request.user:
            return JsonResponse({'error': 'Unauthorized request.'}, status=403)

        if friendship_request.status == FriendshipRequest.ACCEPTED:
            return JsonResponse({'error': 'Запрос уже принят.'}, status=400)

        if friendship_request.status == FriendshipRequest.REJECTED:
            return JsonResponse({'error': 'Запрос был отклонен.'}, status=400)

        friendship_request.status = FriendshipRequest.ACCEPTED
        friendship_request.created_by.friends.add(friendship_request.created_for)
        friendship_request.created_for.friends.add(friendship_request.created_by)


        friendship_request.delete()

        return JsonResponse({'success': 'Запрос принят и вы теперь друзья!'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
@login_required(login_url='/accounts/login/')
def remove_friend(request, user_id):
    user_to_remove = get_object_or_404(PinklerUser, id=user_id)
    if request.user.is_friends_with(user_to_remove):
        request.user.remove_friend(user_to_remove)
        return JsonResponse({'success': 'Друг удален.'})
    return JsonResponse({'error': 'Вы не являетесь друзьями с этим пользователем.'}, status=400)




@csrf_exempt
@login_required(login_url='/accounts/login/')
def reject_friend_request(request, request_id):
    try:
        if request.method != "POST":
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

        friendship_request = get_object_or_404(FriendshipRequest, id=request_id)

        if friendship_request.created_for != request.user:
            return JsonResponse({'error': 'Unauthorized request.'}, status=403)

        if friendship_request.status in [FriendshipRequest.ACCEPTED, FriendshipRequest.REJECTED]:
            return JsonResponse({'error': 'Запрос уже отклонен или принят.'}, status=400)

        friendship_request.delete()

        return JsonResponse({'success': 'Запрос отклонен и удален!'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def cancel_friend_request(request, user_id):
    try:
        if request.method != "POST":
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

        friendship_request = get_object_or_404(FriendshipRequest, id=user_id)

        if friendship_request.created_by != request.user:
            return JsonResponse({'error': 'Unauthorized request.'}, status=403)

        if friendship_request.status in [FriendshipRequest.ACCEPTED, FriendshipRequest.REJECTED]:
            return JsonResponse({'error': 'Запрос уже отклонен или принят.'}, status=400)

        friendship_request.delete()

        return JsonResponse({'success': 'Запрос отклонен и удален!'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/accounts/login/')
def friends_view(request):
    self_friends = request.user.friends.all()
    self_pending = PinklerUser.objects.filter(
        id__in=FriendshipRequest.objects.filter(
            created_for=request.user, status=FriendshipRequest.SENT
        ).values_list('created_by', flat=True)
    )
    self_requested = FriendshipRequest.objects.filter(created_by=request.user,
                                                      status=FriendshipRequest.SENT).values_list('created_for',
                                                                                                 flat=True)
    self_received = FriendshipRequest.objects.filter(created_for=request.user,
                                                     status=FriendshipRequest.SENT).values_list('created_by', flat=True)

    context = {
        'self_friends': self_friends,
        'self_pending': self_pending,
        'self_requested': self_requested,
        'self_received': self_received,
    }
    return render(request, 'friends/friends.html', context)
