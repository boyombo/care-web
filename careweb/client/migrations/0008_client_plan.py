# Generated by Django 2.2.6 on 2019-11-15 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('client', '0007_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Plan'),
        ),
    ]
