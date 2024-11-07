from django.shortcuts import redirect, render


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('feed/')
    else:
        return redirect('accounts/register')


def test(request):
    return render(request, 'users/token_invalid.html')


def tmp_friends_view(request):
    return render(request, 'friends/friends.html')


def tmp_bookmarks_view(request):
    return render(request, 'bookmarks/bookmarks.html')
