# Generated by Django 2.2.6 on 2019-11-11 19:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('reference', models.CharField(blank=True, max_length=200)),
                ('status', models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Failed'), (2, 'Successful')], default=0)),
            ],
        ),
    ]