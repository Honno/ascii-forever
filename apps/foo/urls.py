from django.urls import path

from .views import *


app_name = "foo"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("upload/", UploadView.as_view(), name="upload"),
]
