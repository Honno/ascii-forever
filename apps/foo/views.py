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
    fields = ["title", "text"]
    template_name = "upload.html"

    def post(self, req):
        try:
            title = req.POST["title"]
            text = req.POST["text"]
        except KeyError as e:
            key = e.args[0]

            return render(
                req,
                "upload.html",
                {"err": f"No {key} was given :o"},
            )

        art = Art(title=title, text=text, timestamp=timezone.now())
        art.save()

        return HttpResponseRedirect(reverse("foo:index"))
