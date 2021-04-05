from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class ArtAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Metadata", {"fields": ["title", "timestamp"]}),
        ("Art", {"fields": ["text"]}),
    ]
    list_display = ("title", "timestamp")
    list_filter = ["timestamp"]
    search_fields = ["title"]


admin.site.register(User, UserAdmin)
admin.site.register(Art, ArtAdmin)
