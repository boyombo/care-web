# Generated by Django 2.2.6 on 2019-11-14 10:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ranger', '0003_walletfunding'),
        ('client', '0006_auto_20191111_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('ranger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ranger.Ranger')),
            ],
        ),
    ]