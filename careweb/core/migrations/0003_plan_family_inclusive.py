# Generated by Django 2.2.6 on 2019-12-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191211_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='family_inclusive',
            field=models.BooleanField(default=True),
        ),
    ]
