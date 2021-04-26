import re
from uuid import uuid4
from itertools import takewhile
from pathlib import Path
from io import BytesIO

from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.conf import settings
from django.db.models import *
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property
from PIL import Image, ImageDraw, ImageFont

__all__ = ["User", "Art", "Comment"]


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


thumb_font_path = Path(__file__).parent / "SourceCodePro-Regular.ttf"


THUMB_W = 80
THUMB_H = 19


class Art(Model):
    artist = ForeignKey(User, on_delete=PROTECT)
    text = TextField(validators=[validate_text])

    title = CharField(max_length=80, validators=[validate_text])
    description = TextField(null=True, blank=True, validators=[validate_text])
    timestamp = DateTimeField(default=timezone.now)

    nsfw = BooleanField()

    thumb_x_offset = IntegerField(default=0)
    thumb_y_offset = IntegerField(default=0)

    thumb_render = ImageField(upload_to="thumbs", default="thumbs/default.png")
    uuid = UUIDField(default=uuid4, unique=True)

    likes = ManyToManyField(User, related_name="likes")

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

    def render_thumb(self):
        image = Image.new("RGB", (1200, 628), (255, 255, 255))
        font = ImageFont.truetype(thumb_font_path.as_posix(), size=24)
        dwg = ImageDraw.Draw(image)
        dwg.multiline_text((25, 8), self.renderable_thumb, font=font, spacing=8, fill=(33, 33, 33))

        buf = BytesIO()
        image.save(buf, "PNG")

        return buf

    @cached_property
    def description_preview(self):
        if not self.description:
            return None
        else:
            return "".join(takewhile(lambda c: c != "\n", self.description))

    def clean(self):
        if (
                not - THUMB_W < self.thumb_x_offset < self.w or
                not - THUMB_H < self.thumb_y_offset < self.h
        ):
            raise ValidationError("thumbnail is out-of-bounds")

        if r_nothing.match(self.renderable_thumb):
            raise ValidationError("thumbnail contains only whitespace")

    def save(self, *args, **kwargs):
        thumb_fname = f"{self.uuid}.png"
        thumb_bytes = self.render_thumb()
        thumb_f = ImageFile(thumb_bytes)
        self.thumb_render.save(thumb_fname, thumb_f, save=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:art", args=[str(self.pk)])

    def __str__(self):
        return self.title


# ------------------------------------------------------------------------------
# Comment


class Comment(Model):
    art = ForeignKey(Art, on_delete=PROTECT)
    author = ForeignKey(User, on_delete=PROTECT)
    text = TextField(validators=[validate_text])

    timestamp = DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("core:art", args=[str(self.art.pk)])

    def __str__(self):
        return self.text
