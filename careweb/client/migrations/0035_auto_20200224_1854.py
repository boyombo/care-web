# Generated by Django 2.2.8 on 2020-02-24 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0034_tempclientupload_driver_license'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempclientupload',
            old_name='driver_license',
            new_name='drivers_license',
        ),
    ]
