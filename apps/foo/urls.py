from django.urls import path

from .views import *


app_name = "foo"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("join/", JoinView.as_view(), name="join"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("upload/", UploadView.as_view(), name="upload"),
]
