# Generated by Django 3.2.9 on 2022-05-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_alter_product_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="rating",
            field=models.CharField(max_length=100),
        ),
    ]
