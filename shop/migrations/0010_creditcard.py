# Generated by Django 4.2 on 2024-04-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_category_id_alter_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=100)),
                ('expiry_date', models.CharField(max_length=7)),
                ('security_number', models.CharField(max_length=3)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]
