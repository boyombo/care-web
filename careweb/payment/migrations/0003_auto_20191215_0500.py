# Generated by Django 2.2.6 on 2019-12-15 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20191120_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='narration',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_by',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_mode',
            field=models.PositiveIntegerField(choices=[(0, 'Bank'), (1, 'Card'), (2, 'Fund Request')], null=True),
        ),
    ]
