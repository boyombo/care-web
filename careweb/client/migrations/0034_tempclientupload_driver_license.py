# Generated by Django 2.2.8 on 2020-02-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0033_auto_20200224_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempclientupload',
            name='driver_license',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
