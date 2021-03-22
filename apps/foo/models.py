from django.db.models import *
from django.utils import timezone

__all__ = ["Art"]


class Art(Model):
    title = CharField(max_length=80, default="art")
    text = TextField()
    timestamp = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


