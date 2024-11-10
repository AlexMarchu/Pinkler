from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import PinklerUser
from .forms import CommentModelForm, PostModelForm
from .models import Post, Like


@login_required(login_url='/accounts/register/')
def create_post_list(request):
    query_set = Post.objects.prefetch_related("comments").all()
    # comment_list = [post.comments.all() for post in query_set]
    pinkler_user = PinklerUser.objects.get(username=request.user.username)
    post_form = PostModelForm()
    comment_form = CommentModelForm()

    if 'post_button' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = pinkler_user
            instance.save()
            return redirect('feed:feed')
        
    if 'comment_button' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = pinkler_user
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()

            query_set = Post.objects.prefetch_related("comments").all()
            return redirect('feed:feed')


    context = {
        'query_set': query_set, 
        'pinkler_user': pinkler_user, 
        'post_form': post_form,
        'comment_form': comment_form,
    }

    return render(request, 'feed/feed.html', context)

@login_required(login_url='/accounts/register/')
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        pinkler_user = PinklerUser.objects.get(username=user.username)

        like, created = Like.objects.get_or_create(user=pinkler_user, post_id=post_id)

        if created:
            like.value = 'Like'
            post_obj.liked.add(pinkler_user)
            liked = True
        else:
            if like.value == 'Like':
                like.value = 'Unlike'
                post_obj.liked.remove(pinkler_user)
                liked = False
            else:
                like.value = 'Like'
                post_obj.liked.add(pinkler_user)
                liked = True
            
        post_obj.save()
        like.save()

    return JsonResponse({
            'liked': liked,
            'number_of_likes': post_obj.liked.count(),
        })

@login_required(login_url='/accounts/register/')
def bookmark_view(request):
    post_id = request.POST.get('post_id')
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        pinkler_user = PinklerUser.objects.get(username=user.username)

        if pinkler_user in post_obj.bookmark.all():
            post_obj.bookmark.remove(pinkler_user)
            bookmarked = False
        else:
            post_obj.bookmark.add(pinkler_user)
            bookmarked = True
            
        post_obj.save()

    return JsonResponse({'bookmarked': bookmarked})