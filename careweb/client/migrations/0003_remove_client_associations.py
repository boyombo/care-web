# Generated by Django 2.2.6 on 2019-10-29 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='associations',
        ),
    ]
