# Generated by Django 2.2.8 on 2020-06-20 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0047_auto_20200521_1235'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider', '0004_auto_20200619_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderComment',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('doctor', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('dependant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Dependant')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.CareProvider')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProviderComment',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('doctor', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.Client')),
                ('dependant', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.Dependant')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='provider.CareProvider')),
            ],
            options={
                'verbose_name': 'historical provider comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
