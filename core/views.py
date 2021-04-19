import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User

from .models import *
from .forms import *

__all__ = [
    "IndexView",
    "UserView",
    "UserListView",
    "JoinView",
    "SignInView",
    "SignOutView",
    "ArtView",
    "like_art",
    "ArtGalleryView",
    "PostArtView",
    "ArtEditView",
]


class IndexView(ListView):
    template_name = "core/pages/index.html"
    context_object_name = "arts"
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
          following = user.following.all()

          return (
              Art.objects
              .filter(artist__in=following)
              .order_by("-timestamp")
          )

        else:
            return []


class UserView(DetailView):
    template_name = "core/pages/user.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def post(self, request, username):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            follow_user = json.load(request)["follow_user"]

            follower = request.user
            target = self.get_object()
            if follow_user:
                follower.following.add(target)
            else:
                follower.following.remove(target)

            user_followed = target in follower.following.all()

            return JsonResponse({"user_followed": user_followed})

        else:
            return super().post(request, username)


class UserListView(ListView):
    template_name = "core/pages/users.html"
    context_object_name = "users"
    paginate_by = 100

    def get_queryset(self):
        return (
              User.objects
              .order_by("username")
        )


class JoinView(CreateView):
    template_name = "core/pages/join.html"
    form_class = JoinForm

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("core:user", args=[self.request.user.username])


class SignInView(LoginView):
    template_name = "core/pages/sign_in.html"

    def get_success_url(self):
        return reverse("core:user", args=[self.request.user.username])


class SignOutView(LogoutView):
    next_page = reverse_lazy("core:index")


class ArtView(ModelFormMixin, TemplateView):
    template_name = "core/pages/art.html"
    form_class = CommentForm

    def get_context_data(self, pk):
        art = get_object_or_404(Art, pk=pk)
        comments = art.comment_set.all()

        ctx = {
            "art": art,
            "comments": comments,
            "comment_form": self.get_form(),
        }

        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        else:
            return HttpResponse("Unauthorized", status=401)

        form.instance.art = get_object_or_404(Art, pk=self.kwargs["pk"])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:art", args=[self.kwargs["pk"]])


@require_POST
@login_required
def like_art(request, pk):
    art = get_object_or_404(Art, pk=pk)

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        raise Http404()

    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    like = json.load(request)["like"]

    if like:
        art.likes.add(request.user)
    else:
        art.likes.remove(request.user)

    like_tally = art.likes.count()
    art_liked = request.user in art.likes.all()

    return JsonResponse({"like_tally": like_tally, "art_liked": art_liked})


class ArtGalleryView(ListView):
    template_name = "core/pages/arts.html"
    context_object_name = "arts"
    paginate_by = 25

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-timestamp")
        )


class PostArtView(LoginRequiredMixin, CreateView):
    template_name = "core/pages/post_art.html"
    form_class = ArtForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.artist = self.request.user
        else:
            return HttpResponse("Unauthorized", status=401)

        return super().form_valid(form)


class ArtEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "core/pages/edit.html"
    form_class = ArtForm
    context_object_name = "art"

    def test_func(self):
        art = self.get_object()
        user_is_artist = art.artist == self.request.user

        return user_is_artist

    def get_object(self):
        return get_object_or_404(Art, pk=self.kwargs["pk"])
