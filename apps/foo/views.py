from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Art
from .forms import ArtForm

__all__ = ["IndexView", "JoinView", "SignInView", "UploadView"]


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "arts"

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-timestamp")[:10]
        )


class JoinView(CreateView):
    template_name = "join.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("foo:index")


class SignInView(LoginView):
    template_name = "signin.html"


class UploadView(LoginRequiredMixin, CreateView):
    template_name = "upload.html"
    form_class = ArtForm
    success_url = reverse_lazy("foo:index")

    def form_valid(self, form):
        form.instance.artist = self.request.user

        return super().form_valid(form)
