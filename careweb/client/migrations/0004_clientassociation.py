# Generated by Django 2.2.6 on 2019-10-29 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_client_associations'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Association')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
            ],
        ),
    ]
