# Generated by Django 5.0.2 on 2024-02-11 23:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
