from datetime import timedelta
from typing import NamedTuple

from django.utils import timezone
from pytest import mark

from core.models import *

delta = timedelta(seconds=5)


def assert_now(dt):
    now = timezone.now()

    assert now - delta < dt < now + delta


def create_object(model: str, django_user_model):
    artist = django_user_model.objects.create(username="bob", password="pass")

    if model == "User":
        return artist

    art = Art(artist=artist, title="foo", text="bar", nsfw=False)
    art.save()

    if model == "Art":
        return art

    author = django_user_model.objects.create(username="alice", password="pass")
    comment = Comment(author=author, art=art, text="foo")
    comment.save()

    if model == "Comment":
        return comment


@mark.parametrize("model", ["User", "Art", "Comment"])
@mark.django_db
def test_timestamped_model(model, django_user_model):
    instance = create_object(model, django_user_model)

    assert_now(instance.created_at)
    assert instance.updated_at is None
    assert instance.deleted_at is None
    assert not instance.updated
    assert not instance.deleted

    created_at = instance.created_at

    instance.title = "bar"
    instance.save()

    assert instance.created_at == created_at
    assert_now(instance.updated_at)
    assert instance.deleted_at is None
    assert instance.updated
    assert not instance.deleted

    updated_at = instance.updated_at

    instance.delete()

    assert instance.created_at == created_at
    assert instance.updated_at != instance.deleted_at
    assert instance.updated_at == updated_at
    assert_now(instance.deleted_at)
    assert instance.updated
    assert instance.deleted
