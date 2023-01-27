# Generated by Django 4.1.3 on 2023-01-27 07:35

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import products.models
import products.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('additional_data', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closed', models.BooleanField(default=False)),
                ('contract_number', models.PositiveSmallIntegerField(default=products.models.determine_a_next_contract_number, unique=True, validators=[products.validators.validate_contract_number_format])),
                ('amount', models.FloatField(default=0.0)),
                ('payment_due', models.DateTimeField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='persons.client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Forthcoming'), (2, 'In progress'), (3, 'Finished')], default=1, editable=False)),
                ('start_event', models.DateTimeField(default=datetime.datetime(2023, 1, 27, 9, 35, 1, 490846, tzinfo=datetime.timezone.utc), validators=[products.validators.validate_datetime_no_past])),
                ('end_event', models.DateTimeField(validators=[products.validators.validate_datetime_no_past])),
                ('attendees', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(2)])),
                ('notes', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='products.contract')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='additional_data.location')),
                ('support_employee', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='accounts.supportteamemployee')),
            ],
        ),
    ]
