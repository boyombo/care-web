# Generated by Django 2.2.6 on 2019-12-08 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_auto_20191206_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]