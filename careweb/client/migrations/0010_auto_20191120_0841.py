# Generated by Django 2.2.6 on 2019-11-20 08:41

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_subscription_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False),
        ),
    ]
