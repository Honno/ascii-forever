from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView
from django.utils import timezone

from .models import Art

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
    model = Art
    fields = ["text"]
    template_name = "upload.html"

    def post(self, req):
        try:
            text = req.POST["text"]
        except KeyError:
            return render(
                req,
                "upload.html",
                {"err": "No text was uploaded :o"},
            )

        art = Art(text=text, timestamp=timezone.now())
        art.save()

        return HttpResponseRedirect(reverse("foo:index"))
