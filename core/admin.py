from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class ArtAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Metadata", {"fields": ["artist", "title", "created_at", "updated_at"]}),
    ]
    list_display = ("title", "artist", "created_at")
    list_filter = ["created_at"]
    search_fields = ["title"]


admin.site.register(User, UserAdmin)
admin.site.register(Art, ArtAdmin)
