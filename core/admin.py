from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# class CommentInline(admin.StackedInline):
#     model = Comment


# class ArtAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("Metadata", {"fields": ["artist", "title"]}),
#     ]
#     inlines = [CommentInline]
#     list_display = ("title", "artist", "created_at")
#     list_filter = ["created_at"]
#     search_fields = ["title"]


# admin.site.register(User, UserAdmin)
# admin.site.register(Art, ArtAdmin)
