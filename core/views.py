from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post, Like, Comment, Follow, Notification, Message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import ProfileForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@login_required
def feed(request):

    posts = Post.objects.all().order_by("-created_at")

    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()   # ✅ IMPORTANT
    else:
        notif_count = 0

    return render(request, "core/feed.html", {
        "posts": posts,
        "notif_count": notif_count,
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                text=f"{request.user.username} liked your post"
            )

    return JsonResponse({
        "liked": liked,
        "likes_count": post.like_set.count()
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    text = request.POST.get("comment")
    if not text:
        return JsonResponse({"error": "Empty comment"}, status=400)

    comment = Comment.objects.create(
        post=post,
        user=request.user,
        text=text
    )

    if post.author != request.user:
        Notification.objects.create(
            user=post.author,
            text=f"{request.user.username} commented on your post"
        )

    return JsonResponse({
        "username": comment.user.username,
        "text": comment.text
    })


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile).order_by("-created_at")

    return render(request, "core/profile.html", {
        "profile_user": user_profile,
        "posts": posts
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if created:
            Notification.objects.create(
                user=user_to_follow,
                text=f"{request.user.username} started following you"
            )

    return redirect("profile", username=username)



@login_required
def notifications(request):
    notes = request.user.notifications.order_by("-created_at")
    return render(request, "core/notifications.html", {
        "notes": notes
    })

@login_required
def edit_profile(request):
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile", request.user.username)

    return render(request, "core/edit_profile.html", {"form": form})

@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )

    return render(request, "core/chat.html", {
        "messages": messages,
        "other_user": other_user
    })

def load_posts(request):
    page = int(request.GET.get("page", 1))
    size = 5
    start = (page - 1) * size
    end = page * size

    posts = Post.objects.all().order_by("-created_at")[start:end]

    data = []
    for post in posts:
        data.append({
            "author": post.author.username,
            "content": post.content,
        })

    return JsonResponse(data, safe=False)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_feed(request):
    posts = Post.objects.all().order_by("-created_at")[:20]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(["POST"])
def api_login(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    return Response({"error": "Invalid credentials"}, status=400)

from .models import Post, Notification