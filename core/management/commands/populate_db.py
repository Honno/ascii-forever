from random import Random
from itertools import zip_longest
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.utils.timezone import get_current_timezone
import lorem

from core.models import *


rng = Random()
data_dir = Path(__file__).resolve().parents[1] / "data"


def create_usernames(n=100):
    names = {}

    try:
        with open(data_dir / "first_names.txt") as f:
            names["first"] = f.readlines()

        with open(data_dir / "last_names.txt") as f:
            names["last"] = f.readlines()

    except FileNotFoundError as e:
        raise CommandError("first_names.txt and last_names.txt required") from e

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
    try:
        for path in Path(data_dir / "art").iterdir():
            with open(path) as f:
                art = f.read()

                yield slugify(path.name), art

    except FileNotFoundError as e:
        raise CommandError("art folder required")


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

        users = []
        for id, username in enumerate(usernames, 1):
            user = User(id=id, username=username, password=password)
            users.append(user)

        User.objects.bulk_create(users)

        bob = User.objects.get(username="bob")
        alice = User.objects.get(username="alice")

        admin.following.add(bob)
        admin.following.add(alice)

        dt_start = datetime(1970, 1, 1)
        dt_end = datetime.now()
        dt_diff = dt_end - dt_start
        tz = get_current_timezone()

        arts = []
        comments = []
        for base_id, (fname, art) in enumerate(get_art()):
            naive_dt = dt_start + rng.random() * dt_diff
            dt = tz.localize(naive_dt)

            rand_user = rng.choice(users)

            artists = [rand_user, admin, bob, alice]
            for step, user in enumerate(artists):
                id = base_id * len(artists) + step
                art_obj = Art(id=id, artist=user, title=fname, text=art, timestamp=dt)

                arts.append(art_obj)

                ncomments = rng.randint(0, 50)
                for _ in range(ncomments):
                    rand_author = rng.choice(users)
                    text = lorem.paragraph()
                    comment = Comment(art=art_obj, author=rand_author, text=text)

                    comments.append(comment)

        Art.objects.bulk_create(arts)
        Comment.objects.bulk_create(comments)

