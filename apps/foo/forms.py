import re

from django.forms import *

from .models import Art

__all__ = ["ArtForm"]


r_nothing = re.compile("^\s+$")
r_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)


class ArtTextarea(Widget):
    template_name = "foo/widgets/art_textarea.html"

    def __init__(self, attrs=None):
        default_attrs = {"cols": "80", "rows": "24"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ArtCharField(CharField):
    widget = ArtTextarea

    def clean(self, value):
        try:
            # potential problem:
            # 1. dot purposely added as the first char
            # 2. script to prepend dot didn't work
            # 3. ???
            # 4. GOODBYE DOT
            if value[0] == ".":
                value = value[1:]
        except IndexError:
            raise ValidationError("no text was submitted")

        if not value:
            raise ValidationError("no text was submitted")

        if r_nothing.match(value):
            raise ValidationError("only whitespace was submitted")

        if r_nothing.match(value):
            raise ValidationError("only whitespace was submitted")

        if r_emoji.search(value):
            raise ValidationError("no one is allowed to use emojis except me 😈")

        return value


class ArtForm(ModelForm):
    text = ArtCharField()

    class Meta:
        model = Art
        fields = ["title", "text"]

    class Media:
        js = ("foo/preserve_whitespace.js",)
