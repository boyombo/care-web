# Generated by Django 2.2.8 on 2020-02-13 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0026_auto_20200213_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='verification_code_verified',
        ),
    ]
