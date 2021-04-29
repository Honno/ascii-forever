from django.forms import *
from django.contrib.auth.forms import UserCreationForm

from .models import *

__all__ = ["JoinForm", "ArtForm", "CommentForm"]


# ------------------------------------------------------------------------------
# UserCreationForm


class JoinForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


# ------------------------------------------------------------------------------
# ArtForm


class ArtForm(ModelForm):
    text = CharField()
    js_enabled = BooleanField(required=False, widget=HiddenInput)
    description = CharField(required=False)

    class Meta:
        model = Art
        fields = [
            "title",
            "text",
            "thumb_x_offset",
            "thumb_y_offset",
            "nsfw",
            "description",
        ]

    def clean(self):
        data = super().clean()

        if data.get("js_enabled", False):
            # potential problem:
            # 1. dot purposely added as the first char
            # 2. script to prepend dot didn't work
            # 3. ???
            # 4. GOODBYE DOT
            if data["text"][0] == ".":
                data["text"] = data["text"][1:]

        return data


# ------------------------------------------------------------------------------
# CommentForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
