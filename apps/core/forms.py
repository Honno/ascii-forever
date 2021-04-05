import re

from django.forms import *
from django.contrib.auth.forms import UserCreationForm

from .models import *

__all__ = ["JoinForm", "ArtForm"]


# ------------------------------------------------------------------------------
# UserCreationForm


class JoinForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


# ------------------------------------------------------------------------------
# ArtForm


r_nothing = re.compile("^\s+$")
r_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)


class ArtTextarea(Widget):
    template_name = "core/widgets/art_textarea.html"

    def __init__(self, attrs=None):
        default_attrs = {"cols": "80", "rows": "24"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ArtCharField(CharField):
    widget = ArtTextarea


class ArtForm(ModelForm):
    text = ArtCharField()
    js_enabled = BooleanField(required=False, widget=HiddenInput())

    class Meta:
        model = Art
        fields = ["title", "text"]

    class Media:
        js = ("core/preserve_whitespace.js",)

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

            if not data["text"]:
                raise ValidationError("no text was submitted")

        if r_nothing.match(data["text"]):
            raise ValidationError("only whitespace was submitted")

        if r_nothing.match(data["text"]):
            raise ValidationError("only whitespace was submitted")

        if r_emoji.search(data["text"]):
            raise ValidationError("no one is allowed to use emojis except me 😈")

        return data
