# Generated by Django 3.1.7 on 2021-04-08 10:00

from django.db import migrations
from django.db import models

import core.models

# noop now non-existent validator so migration works
core.models.validate_text = lambda x: None


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="art",
            name="text",
            field=models.TextField(validators=[core.models.validate_text]),
        ),
        migrations.AlterField(
            model_name="art",
            name="title",
            field=models.CharField(
                max_length=80, validators=[core.models.validate_text]
            ),
        ),
    ]
