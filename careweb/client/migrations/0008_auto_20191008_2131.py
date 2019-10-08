# Generated by Django 2.2.6 on 2019-10-08 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_auto_20191008_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='ranger',
            name='lga',
        ),
        migrations.AlterField(
            model_name='client',
            name='pcp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.CareProvider'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ranger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ranger.Ranger'),
        ),
        migrations.AlterField(
            model_name='dependant',
            name='pcp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.CareProvider'),
        ),
        migrations.DeleteModel(
            name='CareProvider',
        ),
        migrations.DeleteModel(
            name='LGA',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Ranger',
        ),
    ]
