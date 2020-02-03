# Generated by Django 2.2.6 on 2020-01-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0020_myclient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'My Client'},
        ),
        migrations.AlterModelOptions(
            name='myclient',
            options={'verbose_name_plural': 'All Clients'},
        ),
        migrations.AddField(
            model_name='client',
            name='subscription_rate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]