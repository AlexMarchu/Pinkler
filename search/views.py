from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from feed.forms import CommentModelForm
from feed.models import Post
from users.models import PinklerUser
from friends.models import FriendshipRequest
from fuzzywuzzy import fuzz

@login_required(login_url='/accounts/login/')
def search_view(request):
    query = request.GET.get('q', '')
    if 'comment_button' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = request.user
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()

            request.POST = ''
            return search_view(request)

    users = PinklerUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
    posts = []
    if query:
        for post in Post.objects.all():
            if fuzz.partial_token_set_ratio(query, post.content.casefold()) > 70:
                posts.append(post)
    else:
        posts = Post.objects.all()
    # posts = Post.objects.filter(
    #     Q(author__in=users) | Q(content__icontains=query)
    # )
    comment_form = CommentModelForm()
    self_friends = request.user.friends.all()
    self_requested = FriendshipRequest.objects.filter(created_by=request.user, status=FriendshipRequest.SENT).values_list('created_for', flat=True)
    context = {'users': users, 'self_friends': self_friends, 'self_requested': self_requested, 'posts': posts, "comment_form": comment_form}
    return render(request, 'search/search.html', context)