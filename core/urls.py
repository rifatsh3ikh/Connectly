from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    feed, signup, like_post, add_comment,
    profile, follow_user, notifications,
    chat, load_posts, api_feed, api_login
)

urlpatterns = [
    path("", feed, name="feed"),
    path("signup/", signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("like/<int:post_id>/", like_post, name="like"),
    path("comment/<int:post_id>/", add_comment, name="comment"),
    path("user/<str:username>/", profile, name="profile"),
    path("follow/<str:username>/", follow_user, name="follow"),
    path("notifications/", notifications, name="notifications"),
    path("chat/<str:username>/", chat, name="chat"),
    path("load-posts/", load_posts, name="load_posts"),
    path("api/feed/", api_feed, name="api_feed"),
    path("api/login/", api_login, name="api_login"),

    
]