# Generated by Django 3.2.9 on 2022-05-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_alter_product_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="rating",
            field=models.IntegerField(),
        ),
    ]
