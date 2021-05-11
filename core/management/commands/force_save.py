from django.core.management.base import BaseCommand, CommandError

import core.models

models = [getattr(core.models, name) for name in core.models.__all__]

class Command(BaseCommand):
    help = "Triggers save method for a model's objects"

    def add_arguments(self, parser):
        parser.add_argument("model", type=str)

    def handle(self, *args, **options):
        for model_str, model in [(cls.__name__, cls) for cls in models]:
            if options["model"] == model_str:
                target = model
                break
        else:
            raise CommandError(f"Model {options['model']} not found")

        for obj in target.objects.all():
            obj.save()
