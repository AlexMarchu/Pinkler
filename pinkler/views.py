from django.shortcuts import redirect


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('feed/')
    else:
        return redirect('accounts/register')
