# Generated by Django 2.2.8 on 2020-02-24 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20191120_0846'),
        ('client', '0030_auto_20200219_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tempclientupload',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='client',
            name='lga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.LGA'),
        ),
        migrations.AddField(
            model_name='tempclientupload',
            name='s_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dependant',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]