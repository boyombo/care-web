# Generated by Django 2.2.6 on 2019-11-30 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_delete_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
