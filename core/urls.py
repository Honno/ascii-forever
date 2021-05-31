from django.urls import path

from .views import *

app_name = "core"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("join", JoinView.as_view(), name="join"),
    path("sign_in", SignInView.as_view(), name="sign_in"),
    path("sign_out", SignOutView.as_view(), name="sign_out"),
    path("post_art", PostArtView.as_view(), name="post_art"),
    path("user/", UserListView.as_view(), name="users"),
    path("user/<slug:username>", UserView.as_view(), name="user"),
    path("user/<slug:username>/settings", SettingsView.as_view(), name="settings"),
    path("user/<slug:username>/follow", follow_user, name="follow_user"),
    path("art/", ArtGalleryView.as_view(), name="arts"),
    path("art/<int:pk>", ArtView.as_view(), name="art"),
    path("art/<int:pk>/thumb.png", art_thumb, name="art_thumb"),
    path("art/<int:pk>/like", like_art, name="like_art"),
    path("art/<int:pk>/edit", EditArtView.as_view(), name="edit_art"),
    path("art/<int:pk>/delete", DeleteArtView.as_view(), name="delete_art"),
    path("nsfw_pref", nsfw_pref, name="nsfw_pref"),
    path("edit_comment", edit_comment, name="edit_comment"),
    path("delete_comment", delete_comment, name="delete_comment"),
]
