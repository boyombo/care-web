# Generated by Django 2.2.6 on 2019-10-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20191023_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='clientphoto'),
        ),
    ]
