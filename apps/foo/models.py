from django.db.models import *

__all__ = ["Art"]


class Art(Model):
    title = CharField(max_length=80, default="art")
    text = TextField()
    timestamp = DateTimeField()

    def __str__(self):
        return self.title


