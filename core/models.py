import re

from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import *
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property

__all__ = ["User", "Art"]


# ------------------------------------------------------------------------------
# User


r_alpha = re.compile("[a-zA-Z]", re.ASCII)
r_slug = re.compile("[a-zA-Z0-9_]+", re.ASCII)
r_alphanumeric = re.compile("[a-zA-Z0-9]", re.ASCII)


class CIUserManager(UserManager):
    def get_by_natural_key(self, username):
        field = f"{self.model.USERNAME_FIELD}__iexact"

        return self.get(**{field: username})


def validate_username(username):
    if not r_slug.fullmatch(username):
        raise ValidationError("must only contain ASCII letters, numbers, and underscores")

    if not r_alpha.match(username[0]):
        raise ValidationError("first character must be a letter")

    if not r_alphanumeric.match(username[-1]):
        raise ValidationError("last character must be a letter or number")


class User(AbstractUser):
    objects = CIUserManager()
    username_validator = validate_username

    username = CharField(
        max_length=20,
        unique=True,
        validators=[validate_username],
    )
    following = ManyToManyField("self", related_name="following")

    def get_absolute_url(self):
        return reverse("core:user", args=[self.username])

    def __str__(self):
        return self.username


# ------------------------------------------------------------------------------
# Art


r_nothing = re.compile("^\s+$")
r_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)


def validate_text(text):
    if len(text) == 0:
        raise ValidationError("no text was submitted")

    if r_nothing.match(text):
        raise ValidationError("only whitespace was submitted")

    if r_emoji.search(text):
        raise ValidationError("no one is allowed to use emojis except me 😈")


THUMB_W = 80
THUMB_H = 19


class Art(Model):
    artist = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=80, validators=[validate_text])
    text = TextField(validators=[validate_text])
    timestamp = DateTimeField(default=timezone.now)

    thumb_x_offset = IntegerField(default=0)
    thumb_y_offset = IntegerField(default=0)

    @cached_property
    def w(self):
        text_lines = self.text.splitlines()

        widths = [len(line) for line in text_lines]
        width = max(widths)

        return width

    @cached_property
    def h(self):
        text_lines = self.text.splitlines()

        height = len(text_lines)

        return height

    @cached_property
    def renderable_thumb(self):
        text_lines = self.text.splitlines()
        thumb_lines = []

        for y in range(self.thumb_y_offset, self.thumb_y_offset + THUMB_H):
            line = ""
            for x in range(self.thumb_x_offset, self.thumb_x_offset + THUMB_W):
                if y >= 0 and x >= 0:
                    try:
                        line += text_lines[y][x]
                    except IndexError:
                        line += " "
                else:
                    line += " "

            thumb_lines.append(line)

        thumb = "\n".join(thumb_lines)

        return thumb

    @cached_property
    def native_thumb(self):
        if self.w < THUMB_W and self.h < THUMB_H:
            return self.text
        else:
            return self.renderable_thumb

    def clean(self):
        if (
                not - THUMB_W < self.thumb_x_offset < self.w or
                not - THUMB_H < self.thumb_y_offset < self.h
        ):
            raise ValidationError("thumbnail is out-of-bounds")

        if r_nothing.match(self.renderable_thumb):
            raise ValidationError("thumbnail contains only whitespace")

    def get_absolute_url(self):
        return reverse("core:art", args=[str(self.pk)])

    def __str__(self):
        return self.title
