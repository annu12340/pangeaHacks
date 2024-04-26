# Generated by Django 4.2.11 on 2024-04-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Qrcode_info",
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
                ("parent", models.CharField(default="", max_length=40)),
                ("childname", models.CharField(max_length=30)),
                ("relationship", models.CharField(max_length=50)),
                ("streetaddress", models.CharField(max_length=50)),
                ("towncity", models.CharField(max_length=50)),
                ("postcode", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=30)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("reports", models.FileField(blank=True, upload_to="reports")),
            ],
        ),
    ]
