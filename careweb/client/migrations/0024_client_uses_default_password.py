# Generated by Django 2.2.8 on 2020-02-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0023_merge_20200203_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='uses_default_password',
            field=models.BooleanField(default=False),
        ),
    ]
