# Generated by Django 2.2.8 on 2020-02-02 16:18

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
            name='international_passport_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='voters_card_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
