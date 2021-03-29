from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Art
from .forms import ArtForm

__all__ = [
    "IndexView",
    "JoinView",
    "SignInView",
    "SignOutView",
    "AddArtView",
    "UserView",
]


class IndexView(ListView):
    template_name = "foo/index.html"
    context_object_name = "arts"

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-timestamp")[:10]
        )


class JoinView(CreateView):
    template_name = "foo/join.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("foo:index")


class SignInView(LoginView):
    template_name = "foo/sign_in.html"


class SignOutView(LogoutView):
    template_name = "foo/sign_out.html"


class AddArtView(LoginRequiredMixin, CreateView):
    template_name = "foo/add.html"
    form_class = ArtForm
    success_url = reverse_lazy("foo:index")

    def form_valid(self, form):
        form.instance.artist = self.request.user

        return super().form_valid(form)


class UserView(DetailView):
    template_name = "foo/users/user.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])
