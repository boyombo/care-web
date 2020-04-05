# Generated by Django 2.2.8 on 2020-04-03 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('ranger', '0010_historicalranger_historicalwalletfunding'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0003_historicallga'),
        ('core', '0005_historicalplan_historicalplanrate'),
        ('provider', '0003_historicalcareprovider'),
        ('client', '0043_auto_20200326_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalHMO',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical hmo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDependant',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('surname', models.CharField(max_length=100)),
                ('salutation', models.CharField(blank=True, default='', max_length=100)),
                ('sex', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, default='', max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('relationship', models.PositiveIntegerField(choices=[(0, 'Spouse'), (1, 'Daughter'), (2, 'Son'), (3, 'Others')])),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('primary', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.Client')),
            ],
            options={
                'verbose_name': 'historical dependant',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalClientAssociation',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('association', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.Association')),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.Client')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Association',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalClient',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('surname', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, default='', max_length=100)),
                ('salutation', models.CharField(blank=True, default='', max_length=100)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=10, null=True, verbose_name='Gender')),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced')], max_length=10, null=True)),
                ('national_id_card_no', models.CharField(blank=True, max_length=50, null=True)),
                ('drivers_licence_no', models.CharField(blank=True, max_length=50, null=True)),
                ('voters_card_no', models.CharField(blank=True, max_length=50, null=True)),
                ('international_passport_no', models.CharField(blank=True, max_length=50, null=True)),
                ('lashma_no', models.CharField(blank=True, default='', max_length=50)),
                ('lashma_quality_life_no', models.CharField(blank=True, max_length=50, null=True)),
                ('lagos_resident_no', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=50, null=True)),
                ('whatsapp_no', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('home_address', models.TextField(blank=True, null=True)),
                ('occupation', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('office_address', models.TextField(blank=True, null=True)),
                ('package_option', models.CharField(choices=[('L', 'LASHMA'), ('Q', 'LASHMA QUALITY LIFE')], max_length=50, null=True)),
                ('payment_option', models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('A', 'Annually')], max_length=50, null=True)),
                ('payment_instrument', models.CharField(choices=[('T', 'Transfer'), ('D', 'Debit Card'), ('E', 'E-Wallet'), ('C', 'Cheque'), ('B', 'Bank Deposit')], max_length=20, null=True)),
                ('registration_date', models.DateTimeField(blank=True, editable=False)),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('verification_code', models.CharField(blank=True, max_length=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('verified', models.BooleanField(default=False)),
                ('subscription_rate', models.CharField(blank=True, max_length=100, null=True)),
                ('uses_default_password', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('hmo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='client.HMO')),
                ('lga', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='location.LGA')),
                ('pcp', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='provider.CareProvider')),
                ('plan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Plan')),
                ('ranger', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ranger.Ranger')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical My Client',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAssociation',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical association',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAdhocClient',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ranger.Ranger')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical adhoc client',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
