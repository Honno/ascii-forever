from django.forms import *

from .models import Art

__all__ = ["ArtForm"]


class ArtForm(ModelForm):
    class Meta:
        model = Art
        fields = ["title", "text"]
