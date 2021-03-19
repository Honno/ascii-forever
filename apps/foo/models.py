from django.db.models import *

__all__ = ["Art"]


class Art(Model):
    text = TextField()
    timestamp = DateTimeField()


