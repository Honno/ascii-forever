import json

from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from werkzeug.wsgi import FileWrapper


from .models import *
from .forms import *

__all__ = [
    "IndexView",
    "UserView",
    "UserListView",
    "SettingsView",
    "nsfw_pref",
    "follow_user",
    "JoinView",
    "SignInView",
    "SignOutView",
    "ArtView",
    "art_thumb",
    "like_art",
    "ArtGalleryView",
    "PostArtView",
    "ArtEditView",
]


# ------------------------------------------------------------------------------
# IndexView


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
              .order_by("-created_at")
          )

        else:
            return []


# ------------------------------------------------------------------------------
# Directories


class UserListView(ListView):
    template_name = "core/pages/users.html"
    context_object_name = "users"
    paginate_by = 100

    def get_queryset(self):
        return (
              User.objects
              .order_by("username")
        )


class ArtGalleryView(ListView):
    template_name = "core/pages/arts.html"
    context_object_name = "arts"
    paginate_by = 25

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-created_at")
        )


# ------------------------------------------------------------------------------
# User gateways


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


# ------------------------------------------------------------------------------
# UserView


class ArtGalleryComponent(MultipleObjectMixin):
    context_object_name = "arts"
    paginate_by = 25

    def __init__(self, request, username):
        self.request = request
        self.kwargs = { "username": username }
        self.object_list = self.get_queryset()

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["username"])

        return user.art_set.all().order_by("-created_at")


class UserView(TemplateView):
    template_name = "core/pages/user.html"

    def get(self, request, username):
        self.arts_component = ArtGalleryComponent(request, username)

        return super().get(request, username)

    def get_context_data(self):
        user = get_object_or_404(User, username=self.kwargs["username"])
        ctx = { "user": user }

        arts_ctx = self.arts_component.get_context_data()
        ctx.update(arts_ctx)

        return ctx


# ------------------------------------------------------------------------------
# User upsert


class SettingsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "core/pages/settings.html"
    form_class = SettingsForm
    context_object_name = "user"

    def test_func(self):
        return self.request.user == self.get_object()

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_success_url(self):
        return reverse("core:user", args=[self.get_object().username])


# ------------------------------------------------------------------------------
# ArtView


class ArtView(DetailView):
    template_name = "core/pages/art.html"
    model = Art


# ------------------------------------------------------------------------------
# Art upsert


class PostArtView(LoginRequiredMixin, CreateView):
    template_name = "core/pages/post_art.html"
    form_class = ArtForm

    def form_valid(self, form):
        form.instance.artist = self.request.user

        return super().form_valid(form)


class ArtEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "core/pages/edit.html"
    form_class = ArtForm
    context_object_name = "art"

    def test_func(self):
        return self.request.user == self.get_object().artist

    def get_object(self):
        return get_object_or_404(Art, pk=self.kwargs["pk"])


# ------------------------------------------------------------------------------
# Art thumbnail


def art_thumb(request, pk):
    art = get_object_or_404(Art, pk=pk)
    image = art.render_thumb()

    # https://help.pythonanywhere.com/pages/FlaskSendFileBytesIO/
    wrapped_image = FileWrapper(image)
    response = HttpResponse(wrapped_image, content_type="image/png")
    response["Content-Disposition"] = 'filename="thumb.png"'

    return response


# ------------------------------------------------------------------------------
# Ajax endpoints


def require_ajax(func):
    def wrapper(request, *args, **kwargs):
        if not request.headers.get("x-requested-with") == "XMLHttpRequest":
            raise Http404()

        response = func(request, *args, **kwargs)

        return response

    return wrapper


@require_ajax
@require_GET
def nsfw_pref(request):
    if not request.user.is_authenticated:
        pref = User.nsfw_pref.choices.ALWAYS_ASK
    else:
        pref = request.user.nsfw_pref

    return JsonResponse({"nsfw_pref": pref})



@require_ajax
@require_POST
@login_required
def follow_user(request, username):
    target = get_object_or_404(User, username=username)
    follower = request.user

    follow_user = json.load(request)["follow_user"]
    if follow_user:
        follower.following.add(target)
    else:
        follower.following.remove(target)

    user_followed = target in follower.following.all()

    return JsonResponse({"user_followed": user_followed})


@require_ajax
@require_POST
@login_required
def like_art(request, pk):
    art = get_object_or_404(Art, pk=pk)

    like = json.load(request)["like"]

    if like:
        art.likes.add(request.user)
    else:
        art.likes.remove(request.user)

    like_tally = art.likes.count()
    art_liked = request.user in art.likes.all()

    return JsonResponse({"like_tally": like_tally, "art_liked": art_liked})
