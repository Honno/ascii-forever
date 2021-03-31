from django.conf import settings
from django.db.models import *
from django.utils import timezone

__all__ = ["Art"]


class Art(Model):
    artist = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    title = CharField(max_length=80)
    text = TextField()
    timestamp = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


