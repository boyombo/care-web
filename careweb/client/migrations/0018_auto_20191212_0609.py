# Generated by Django 2.2.6 on 2019-12-12 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_auto_20191211_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependant',
            name='pcp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.CareProvider'),
        ),
    ]
