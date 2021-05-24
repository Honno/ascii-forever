from random import Random
from itertools import zip_longest
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.utils.timezone import get_current_timezone
from django.conf import settings
import lorem

from core.models import *


rng = Random()
data_dir = Path(__file__).resolve().parents[1] / "data"


def get_usernames(n=100):
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
        username = username[:20]

        if rng.getrandbits(1):
            username = username.lower()

        if not username in usernames:
            usernames.append(username)

    for username in ["bob", "alice"]:
        try:
            usernames.remove(username)
        except ValueError:
            pass

    return usernames


def get_art():
    try:
        for path in Path(data_dir / "art").rglob("*"):
            if path.is_file():
                with open(path) as f:
                    art = f.read()

                    yield path.name, art

    except FileNotFoundError as e:
        raise CommandError("art folder required") from e


def sample_pop(sequence, n):
    sample = []
    for _ in range(n):
        i = rng.randrange(len(sequence))
        v = sequence.pop(i)

        sample.append(v)

    return sample


def gen_text():
    nparagraphs = rng.randint(1, 3)
    paragraphs = []
    for _ in range(nparagraphs):
        p = lorem.paragraph()
        paragraphs.append(p)

    join_char = rng.choice(["\n", "\n\n", "\n\n"])
    text = join_char.join(paragraphs)

    return text


tz = get_current_timezone()
dt_epoch = tz.localize(datetime(1970, 1, 1))
dt_now = tz.localize(datetime.now())


def gen_dt(dt_start=dt_epoch):
    dt_diff = dt_now - dt_start
    dt = dt_start + rng.random() * dt_diff

    return dt


class Command(BaseCommand):
    help = "Populates the database for a development environment"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Not in debug mode (don't use this in prod!)")

        if User.objects.exists() or Art.objects.exists():
            raise CommandError("Objects already exist")

        password = make_password("pass")

        admin = User(id=1, username="admin", password=password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        bob = User(id=2, username="bob", password=password)
        bob.save()
        alice = User(id=3, username="alice", password=password)
        alice.save()

        admin.following.add(bob)
        admin.following.add(alice)

        users = []
        for id, username in enumerate(get_usernames(), 4):
            user = User(id=id, username=username, password=password)
            users.append(user)

        User.objects.bulk_create(users)

        raw_arts = list(get_art())

        user_art_samples = [
            (admin, sample_pop(raw_arts, 10)),
            (bob, sample_pop(raw_arts, 10)),
            (alice, sample_pop(raw_arts, 10)),
        ]
        while raw_arts:
            sample_size = rng.randint(1, min(50, len(raw_arts)))
            sample = sample_pop(raw_arts, sample_size)
            user = rng.choice(users)

            user_art_samples.append((user, sample))

        art_id = 1
        arts = []
        comments = []
        for user, sample in user_art_samples:
            for fname, text in sample:
                dt = gen_dt()
                art = Art(
                    id=art_id,
                    artist=user,
                    title=fname,
                    text=text,
                    description=gen_text(),
                    nsfw=rng.choice([True, False]),
                    created_at=dt,
                )
                art_id += 1

                arts.append(art)

                ncomments = rng.randint(0, 50)
                for _ in range(ncomments):
                    author = rng.choice(users)
                    comment = Comment(
                        art=art,
                        author=author,
                        text=gen_text(),
                        created_at=gen_dt(dt_start=dt),
                    )

                    comments.append(comment)

        Art.objects.bulk_create(arts)
        Comment.objects.bulk_create(comments)

        # force native thumbnail generation
        for art in arts:
            art.save()
