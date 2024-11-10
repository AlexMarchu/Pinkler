from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home_view(request):
    return redirect('feed/')

@login_required(login_url='/accounts/login/')
def tmp_bookmarks_view(request):
    return render(request, 'bookmarks/bookmarks.html')