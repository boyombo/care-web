# Generated by Django 2.2.8 on 2020-02-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0021_auto_20200202_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependant',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='dependantphoto'),
        ),
    ]
