from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone

from .models import Art

__all__ = ["IndexView"]


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "arts"

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-timestamp")[:10]
        )

