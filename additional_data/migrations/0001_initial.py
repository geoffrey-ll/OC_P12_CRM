# Generated by Django 4.1.3 on 2023-01-22 05:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siren', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('name', models.CharField(max_length=50)),
                ('designation', models.CharField(default=models.CharField(max_length=50), max_length=50, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nic', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)])),
                ('designation', models.CharField(default=None, max_length=50)),
                ('street_number', models.PositiveSmallIntegerField()),
                ('bis_ter', models.CharField(blank=True, max_length=10, null=True)),
                ('street_name', models.CharField(max_length=50)),
                ('zip_code', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)])),
                ('town_name', models.CharField(max_length=50)),
                ('country', models.CharField(default='France', max_length=50)),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='additional_data.company')),
            ],
        ),
    ]
