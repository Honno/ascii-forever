from django.contrib import admin

from .models import Art

class ArtAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Metadata", {"fields": ["title", "timestamp"]}),
        ("Art", {"fields": ["text"]}),
    ]
    list_display = ("title", "timestamp")
    list_filter = ["timestamp"]
    search_fields = ["title"]

admin.site.register(Art, ArtAdmin)
