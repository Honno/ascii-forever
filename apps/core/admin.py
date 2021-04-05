from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class ArtAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Metadata", {"fields": ["artist", "title", "timestamp"]}),
    ]
    list_display = ("title", "artist", "timestamp")
    list_filter = ["timestamp"]
    search_fields = ["title"]


admin.site.register(User, UserAdmin)
admin.site.register(Art, ArtAdmin)
