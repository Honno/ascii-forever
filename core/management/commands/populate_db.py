from random import Random
from itertools import zip_longest
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.utils.timezone import get_current_timezone

from core.models import *


rng = Random()
data_dir = Path(__file__).resolve().parents[1] / "data"
names = {}

with open(data_dir / "first_names.txt") as f:
    names["first"] = f.readlines()

with open(data_dir / "last_names.txt") as f:
    names["last"] = f.readlines()


def create_usernames(n=100):
    first_names = rng.sample(names["first"], n)

    nlast = rng.randint(0, n)
    last_names = rng.sample(names["last"], nlast)

    usernames = []
    for first, last in zip_longest(first_names, last_names):
        if last is None:
            username = first
        else:
            username = first + " " + last

        username = slugify(username)

        if rng.getrandbits(1):
            username = username.lower()

        if not username in usernames:
            usernames.append(username)

    if "bob" not in usernames:
        usernames.append("bob")
    if "alice" not in usernames:
        usernames.append("alice")

    return usernames


def get_art():
    for path in Path(data_dir / "art").iterdir():
        with open(path) as f:
            art = f.read()

            yield slugify(path.name), art



class Command(BaseCommand):
    help = "Populates the database for a development environment"

    def handle(self, *args, **options):
        if User.objects.exists() or Art.objects.exists():
            raise CommandError("objects already exist")

        password = make_password("pass")

        admin = User(id=0, username="admin", password=password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        usernames = create_usernames()

        try:
            users = []
            for id, username in enumerate(usernames, 1):
                user = User(id=id, username=username, password=password)
                users.append(user)

        except FileNotFoundError as e:
            raise CommandError("first_names.txt and last_names.txt required") from e

        User.objects.bulk_create(users)

        bob = User.objects.get(username="bob")
        alice = User.objects.get(username="alice")

        admin.following.add(bob)
        admin.following.add(alice)

        dt_start = datetime(1970, 1, 1)
        dt_end = datetime.now()
        dt_diff = dt_end - dt_start
        tz = get_current_timezone()

        try:
            arts = []
            for fname, art in get_art():
                user = rng.choice(users)
                naive_dt = dt_start + rng.random() * dt_diff
                dt = tz.localize(naive_dt)

                art_rand = Art(artist=user, title=fname, text=art, timestamp=dt)
                arts.append(art_rand)

                art_admin = Art(artist=admin, title=fname, text=art, timestamp=dt)
                arts.append(art_admin)

                art_bob = Art(artist=bob, title=fname, text=art, timestamp=dt)
                arts.append(art_bob)

                art_alice = Art(artist=alice, title=fname, text=art, timestamp=dt)
                arts.append(art_alice)

        except FileNotFoundError as e:
            raise CommandError("art folder required")

        Art.objects.bulk_create(arts)
