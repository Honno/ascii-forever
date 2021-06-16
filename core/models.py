import re
from functools import lru_cache
from io import BytesIO
from itertools import chain
from itertools import takewhile
from pathlib import Path
from typing import Protocol

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator
from django.db.models import *
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import SafeString
from django.utils.html import escape
from django.utils.timezone import now
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

__all__ = ["User", "Art", "Comment"]


# ------------------------------------------------------------------------------
# Helpers

# Cached methods


@lru_cache
def split_lines(text):
    return text.replace("\r", "").split("\n")


# Validation

r_nothing = re.compile(r"^\s+$")
r_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
r_tab = re.compile("\t")


def validate_whitespace(text):
    if r_nothing.match(text):
        raise ValidationError("only whitespace was submitted")


def validate_emojis(text):
    if r_emoji.search(text):
        raise ValidationError("no one is allowed to use emojis except me 😈")


def validate_tabs(text):
    if r_tab.search(text):
        raise ValidationError("tab characters are not allowed")


text_validators = [
    MinLengthValidator(1, message="No text was submitted."),
    validate_whitespace,
    validate_emojis,
    validate_tabs,
]

# Time stamping


class SoftDeletableQuerySet(QuerySet):
    def delete(self):
        return super().update(deleted_at=now())

    def hard_delete(self):
        return super().delete()


class SoftDeletableManager(Manager):
    _queryset_class = SoftDeletableQuerySet

    def __init__(self, *args, show_deleted=False, **kwargs):
        self.show_deleted = show_deleted
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self._queryset_class(self.model)

        if not self.show_deleted:
            return queryset.filter(deleted_at=None)
        else:
            return queryset


class TimeStampedModelMixin(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(blank=True, null=True)
    deleted_at = DateTimeField(blank=True, null=True)

    objects = SoftDeletableManager()
    _objects = SoftDeletableManager(show_deleted=True)

    class Meta:
        abstract = True

    @property
    def updated(self):
        return bool(self.updated_at)

    @property
    def deleted(self):
        return bool(self.deleted_at)

    def delete(self):
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super().delete()


def update_timestamp(sender, instance, **kwargs):
    # instance.pk i.e. has been created
    if (
        isinstance(instance, TimeStampedModelMixin)
        and instance.pk
        and not instance.deleted
    ):
        instance.updated_at = now()


pre_save.connect(update_timestamp)


# ------------------------------------------------------------------------------
# User


r_alpha = re.compile("[a-zA-Z]", re.ASCII)
r_slug = re.compile("[a-zA-Z0-9_]+", re.ASCII)
r_alphanumeric = re.compile("[a-zA-Z0-9]", re.ASCII)


class CIUserManager(SoftDeletableManager, UserManager):
    def get_by_natural_key(self, username):
        field = f"{self.model.USERNAME_FIELD}__iexact"

        return self.get(**{field: username})


def validate_username(username):
    if not r_slug.fullmatch(username):
        raise ValidationError(
            "Must only contain ASCII letters, numbers, and underscores."
        )


AVATAR_W = 24
AVATAR_H = 16


@lru_cache
def find_width(lines):
    col_lengths = [len(line) for line in lines]
    maxlen = max(col_lengths)

    return maxlen


def validate_avatar_cols(text):
    lines = split_lines(text)
    maxlen = find_width(tuple(lines))
    if maxlen > AVATAR_W:
        raise ValidationError(
            f"Must not exceed {AVATAR_W} columns ({maxlen} cols submitted)"
        )


def validate_avatar_rows(text):
    lines = split_lines(text)
    nlines = len(lines)
    if nlines > AVATAR_H:
        raise ValidationError(
            f"Must not exceed {AVATAR_H} rows ({nlines} rows submitted)"
        )


avatar_validators = [validate_avatar_cols, validate_avatar_rows]


default_avatar = r"""


           ______
         ,'      `.
   /.   /          \
   `.`.:            :
   _.:'|   ,--------|
   `-·´|  | v     v :
       :  \_.---`-._|
    __  \           ;
 ·-´\_\  :         /
     \_\ :  ` . _.´
      \ (        :
 __.---´          `--._
´                      '"""


def pad(string, maxlen):
    nspaces = maxlen - len(string)
    padded_string = string + " " * nspaces

    return padded_string


class NSFWChoices(TextChoices):
    ALWAYS_ASK = "AA"
    SHOW_ALL = "SA"
    HIDE_ALL = "HA"


class User(TimeStampedModelMixin, AbstractUser):
    objects = CIUserManager()
    _objects = CIUserManager(show_deleted=True)

    username = CharField(
        max_length=20,
        unique=True,
        validators=[validate_username],
    )

    avatar = TextField(
        default=default_avatar,
        validators=[*text_validators, *avatar_validators],
    )
    description = TextField(
        blank=True,
        null=True,
        validators=[MaxLengthValidator(100)],
    )

    following = ManyToManyField("self", related_name="following")
    nsfw_pref = CharField(
        max_length=2,
        choices=NSFWChoices.choices,
        default=NSFWChoices.ALWAYS_ASK,
    )

    def get_absolute_url(self):
        return reverse("core:user", args=[self.username])

    def __str__(self):
        return self.username


def pad_avatar(sender, instance: User, **kwargs):
    lines = split_lines(instance.avatar)

    # 1. center horizontally
    maxlen = find_width(tuple(lines))
    ncols_gap = AVATAR_W - maxlen
    if ncols_gap > 1:
        nspaces = ncols_gap // 2
        spaces = " " * nspaces
        lines = [spaces + line for line in lines]

    # 2. center vertically
    nrows_gap = AVATAR_H - len(lines)
    if nrows_gap > 0:
        bottom_nrows = nrows_gap // 2
        top_nrows = nrows_gap - bottom_nrows
        lines = chain(
            ["" for _ in range(top_nrows)],
            lines,
            ["" for _ in range(bottom_nrows)],
        )

    # 3. pad to border
    padded_lines = [pad(line, AVATAR_W) for line in lines]
    padded_avatar = "\n".join(padded_lines)

    instance.avatar = padded_avatar


pre_save.connect(pad_avatar, sender=User)


def user_self_follow(sender, instance: User, created, **kwargs):
    if created:
        instance.following.add(instance)


post_save.connect(user_self_follow, sender=User)


# ------------------------------------------------------------------------------
# Art


thumb_font_path = Path(__file__).parent / "SourceCodePro-Regular.ttf"


THUMB_W = 80
THUMB_H = 19


class Art(TimeStampedModelMixin, Model):
    artist = ForeignKey(User, on_delete=PROTECT)

    text = TextField(validators=text_validators)

    title = CharField(max_length=80, validators=text_validators)
    description = TextField(blank=True, null=True, validators=text_validators)

    nsfw = BooleanField()

    thumb_x_offset = IntegerField(default=0)
    thumb_y_offset = IntegerField(default=0)

    likes = ManyToManyField(User, related_name="likes")

    @cached_property
    def w(self):
        text_lines = split_lines(self.text)

        widths = [len(line) for line in text_lines]
        width = max(widths, default=0)

        return width

    @cached_property
    def h(self):
        text_lines = split_lines(self.text)

        height = len(text_lines)

        return height

    @cached_property
    def wide(self):
        return self.w > THUMB_W

    @cached_property
    def tall(self):
        return self.h > THUMB_H

    @cached_property
    def native_thumb(self) -> SafeString:
        text_lines = split_lines(self.text)
        thumb_lines = []

        if not self.tall:
            y_range = range(self.h)
        else:
            y_range = range(self.thumb_y_offset, self.thumb_y_offset + THUMB_H)

        if not self.wide:
            x_range = range(self.w)
        else:
            x_range = range(self.thumb_x_offset, self.thumb_x_offset + THUMB_W)

        for y in y_range:
            line = ""
            for x in x_range:
                if y >= 0 and x >= 0:
                    try:
                        line += text_lines[y][x]
                    except IndexError:
                        line += " "
                else:
                    line += " "

            thumb_lines.append(line)

        thumb = "\n".join(thumb_lines)

        return escape(thumb)

    @cached_property
    def renderable_thumb(self) -> str:
        text_lines = split_lines(self.text)
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
    def markup(self) -> SafeString:
        return escape(self.text)

    def rasterize_thumb(self):
        image = Image.new("RGB", (1200, 628), (0, 0, 0))
        font = ImageFont.truetype(thumb_font_path.as_posix(), size=24)
        dwg = ImageDraw.Draw(image)
        dwg.multiline_text(
            (25, 8), self.renderable_thumb, font=font, spacing=8, fill=(253, 253, 253)
        )

        buf = BytesIO()
        image.save(buf, "PNG")
        buf.seek(0)

        return buf

    @cached_property
    def description_preview(self):
        if not self.description:
            return None
        else:
            return "".join(takewhile(lambda c: c != "\n", self.description))

    def clean(self):
        if (
            not -THUMB_W < self.thumb_x_offset < self.w
            or not -THUMB_H < self.thumb_y_offset < self.h
        ):
            raise ValidationError("thumbnail is out-of-bounds")

        if r_nothing.match(self.renderable_thumb):
            raise ValidationError("thumbnail contains only whitespace")

    def get_absolute_url(self):
        return reverse("core:art", args=[str(self.pk)])

    def __str__(self):
        return self.title


def artist_self_like(sender, instance: Art, created, **kwargs):
    if created:
        instance.likes.add(instance.artist)


post_save.connect(artist_self_like, sender=Art)


# ------------------------------------------------------------------------------
# Comment


class Comment(TimeStampedModelMixin, Model):
    art = ForeignKey(Art, on_delete=PROTECT)
    author = ForeignKey(User, on_delete=PROTECT)
    text = TextField(validators=text_validators)

    def get_absolute_url(self):
        return reverse("core:art", args=[str(self.art.pk)])

    def __str__(self):
        if len(self.text) < 20:
            return self.text
        else:
            return self.text[:20] + "..."
