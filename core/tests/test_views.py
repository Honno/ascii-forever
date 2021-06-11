from django.urls import reverse
from pytest import mark

from core.models import *

urls = [reverse(name) for name in ["core:index", "core:arts"]]


@mark.parametrize("url", urls)
@mark.django_db
def test_nsfw_filter(url, django_user_model, client):
    target = django_user_model.objects.create(username="bob", password="pass")
    follower = django_user_model.objects.create(username="alice", password="pass")

    follower.following.add(target)

    sfw = PlaintextArt(id=1, artist=target, title="sfw", text="sfw", nsfw=False)
    nsfw = PlaintextArt(id=2, artist=target, title="nsfw", text="nsfw", nsfw=True)

    sfw.save()
    nsfw.save()

    client.force_login(follower)

    response = client.get(url)

    assert sfw in response.context["arts"]
    assert nsfw in response.context["arts"]

    follower.nsfw_pref = "HA"
    follower.save()

    response = client.get(url)

    assert sfw in response.context["arts"]
    assert nsfw not in response.context["arts"]
