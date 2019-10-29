# Generated by Django 2.2.6 on 2019-10-29 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider', '0001_initial'),
        ('ranger', '0002_ranger_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=10, null=True, verbose_name='Gender')),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced')], max_length=10, null=True)),
                ('national_id_card_no', models.CharField(blank=True, max_length=50)),
                ('drivers_licence_no', models.CharField(blank=True, max_length=50)),
                ('lashma_no', models.CharField(blank=True, max_length=50)),
                ('lashma_quality_life_no', models.CharField(blank=True, max_length=50)),
                ('lagos_resident_no', models.CharField(blank=True, max_length=50)),
                ('phone_no', models.CharField(blank=True, max_length=50)),
                ('whatsapp_no', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('home_address', models.TextField(blank=True)),
                ('occupation', models.CharField(blank=True, max_length=200)),
                ('company', models.CharField(blank=True, max_length=200)),
                ('office_address', models.TextField(blank=True)),
                ('package_option', models.CharField(choices=[('L', 'LASHMA'), ('Q', 'LASHMA QUALITY LIFE')], max_length=50, null=True)),
                ('payment_option', models.CharField(choices=[('W', 'Weekly'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('A', 'Annually')], max_length=50, null=True)),
                ('payment_instrument', models.CharField(choices=[('T', 'Transfer'), ('D', 'Debit Card'), ('E', 'E-Wallet'), ('C', 'Cheque'), ('B', 'Bank Deposit')], max_length=20, null=True)),
                ('registration_date', models.DateField(default=django.utils.timezone.now)),
                ('associations', models.ManyToManyField(related_name='client_associations', to='client.Association')),
            ],
        ),
        migrations.CreateModel(
            name='HMO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dependant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('relationship', models.PositiveIntegerField(choices=[(0, 'Spouse'), (1, 'Daughter'), (2, 'Son'), (3, 'Others')])),
                ('pcp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.CareProvider')),
                ('primary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Client')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='hmo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.HMO'),
        ),
        migrations.AddField(
            model_name='client',
            name='pcp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.CareProvider'),
        ),
        migrations.AddField(
            model_name='client',
            name='ranger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ranger.Ranger'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
