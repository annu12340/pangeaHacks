# Generated by Django 4.2.11 on 2024-04-27 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qrcode", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="A",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ads", models.IntegerField()),
            ],
        ),
    ]