# Generated by Django 2.2.8 on 2020-04-03 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_historicallga'),
        ('payment', '0006_historicalpayment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ranger', '0009_ranger_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalWalletFunding',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('payment_type', models.PositiveIntegerField(choices=[(0, 'Bank Transfer'), (1, 'Bank Deposit'), (2, 'Paystack')], default=0)),
                ('status', models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Failed'), (2, 'Successful')], default=0)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payment.Payment')),
                ('ranger', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ranger.Ranger')),
            ],
            options={
                'verbose_name': 'historical wallet funding',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRanger',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=50)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lga', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='location.LGA')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ranger',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
