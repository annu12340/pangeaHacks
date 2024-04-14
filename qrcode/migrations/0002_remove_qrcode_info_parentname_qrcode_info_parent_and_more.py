# Generated by Django 4.2 on 2024-04-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode_info',
            name='parentname',
        ),
        migrations.AddField(
            model_name='qrcode_info',
            name='parent',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='qrcode_info',
            name='postcode',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='qrcode_info',
            name='relationship',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='qrcode_info',
            name='streetaddress',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='qrcode_info',
            name='towncity',
            field=models.CharField(max_length=50),
        ),
    ]