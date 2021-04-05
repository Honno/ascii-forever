import re

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import *
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager

__all__ = ["User", "Art"]


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


class Art(Model):
    artist = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=80)
    text = TextField()
    timestamp = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


