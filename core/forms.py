from django.contrib.auth.forms import UserCreationForm
from django.forms import *

from .models import *

__all__ = [
    "JoinForm",
    "PreferencesForm",
    "ProfileForm",
    "PlaintextArtForm",
    "CommentForm",
]


class JoinForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class PreferencesForm(ModelForm):
    class Meta:
        model = User
        fields = ["nsfw_pref"]


class PreserveWhitespaceModelForm(ModelForm):
    js_enabled = BooleanField(required=False, widget=HiddenInput)

    class Meta:
        preserve_name = None

    def clean(self):
        data = super().clean()

        if data.get("js_enabled", False):
            # potential problem:
            # 1. dot purposely added as the first char
            # 2. script to prepend dot didn't work
            # 3. ???
            # 4. GOODBYE DOT
            if data[self.Meta.preserve_name][0] == ".":
                data[self.Meta.preserve_name] = data[self.Meta.preserve_name][1:]

        return data


class ProfileForm(PreserveWhitespaceModelForm):
    js_enabled = BooleanField(required=False, widget=HiddenInput)

    class Meta:
        model = User
        fields = ["avatar", "description"]

        preserve_name = "avatar"


class PlaintextArtForm(PreserveWhitespaceModelForm):
    class Meta:
        model = PlaintextArt
        fields = [
            "title",
            "text",
            "thumb_x_offset",
            "thumb_y_offset",
            "nsfw",
            "description",
        ]

        preserve_name = "text"


# class UploadArtForm(ModelForm):
#     class Meta:
#         model = Art
#         fields = [
#             "title",
#             "markup",
#             "thumb_x_offset",
#             "thumb_y_offset",
#             "nsfw",
#             "description",
#         ]

#         preserve_name = "markup"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
