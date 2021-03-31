from django.urls import path

from .views import *


app_name = "core"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("join", JoinView.as_view(), name="join"),
    path("sign_in", SignInView.as_view(), name="sign_in"),
    path("sign_out", SignOutView.as_view(), name="sign_out"),
    path("users/<slug:username>", UserView.as_view(), name="user"),
    path("add", AddArtView.as_view(), name="add"),
]
