# Generated by Django 2.2.8 on 2020-02-25 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0035_auto_20200224_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='salutation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dependant',
            name='salutation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dependant',
            name='sex',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
