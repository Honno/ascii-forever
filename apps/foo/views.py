from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils import timezone

from .models import Art
from .forms import ArtForm

__all__ = ["IndexView", "UploadView"]


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "arts"

    def get_queryset(self):
        return (
            Art.objects
            .order_by("-timestamp")[:10]
        )


class UploadView(CreateView):
    template_name = "upload.html"
    form_class = ArtForm
    success_url = reverse_lazy("foo:index")
