# Generated by Django 3.2.9 on 2022-05-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220507_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=4.1, max_digits=2),
        ),
    ]
