import re
from html import unescape

from django.utils.safestring import SafeString
from pytest import fixture
from pytest import mark

from core.models import *

from . import arts
from .multiline import *

button = r"<button>Not a button</button>"
button_safe = r"&lt;button&gt;Not a button&lt;/button&gt;"


@mark.django_db
def test_render_thumb(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=user, title="python logo", text=arts.py_logo)

    multiline_assert(art.renderable_thumb, arts.py_logo_render)


@mark.django_db
def test_native_thumb(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    art = Art(artist=user, title="mrlc's test", text=arts.mrlc_test, nsfw=False)
    art.save()

    multiline_assert(unescape(art.native_thumb), arts.mrlc_test_native)


@mark.django_db
def test_self_like(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    art = Art(artist=user, title="mrlc's test", text=arts.mrlc_test, nsfw=False)
    art.save()

    assert user in art.likes.get_queryset().all()


@mark.django_db
def test_art_delete(django_user_model):
    artist = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=artist, title="python logo", text=arts.py_logo, nsfw=False)
    art.save()

    author = django_user_model.objects.create(username="alice", password="pass")
    comment = Comment(author=author, art=art, text="foo")
    comment.save()

    art.delete()

    assert Art.objects.count() == 0
    assert Art._objects.count() == 1
    assert Comment.objects.count() == 1


@mark.django_db
def test_safe(django_user_model):
    artist = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=artist, title="Not a button", text=button, nsfw=False)
    art.save()

    assert art.native_thumb == button_safe
    assert art.markup == button_safe
