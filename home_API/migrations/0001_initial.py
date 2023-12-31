# Generated by Django 4.2.3 on 2023-07-31 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('formatted_version', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GovernmentalArea',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('formatted_version', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100)),
                ('projectName', models.CharField(max_length=100)),
                ('projectType', models.CharField(max_length=100)),
                ('developerName', models.CharField(max_length=100)),
                ('landParcel', models.FloatField()),
                ('landmark', models.CharField(max_length=100)),
                ('areaIn', models.CharField(max_length=100)),
                ('waterSupply', models.CharField(max_length=100)),
                ('floors', models.IntegerField()),
                ('flatsPerFloors', models.IntegerField()),
                ('totalUnit', models.IntegerField()),
                ('availableUnit', models.IntegerField()),
                ('amenities', models.CharField(max_length=100)),
                ('parking', models.CharField(max_length=100)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('transport', models.BooleanField()),
                ('readyToMove', models.BooleanField()),
                ('power', models.BooleanField()),
                ('goods', models.BooleanField()),
                ('rera', models.DateTimeField()),
                ('possession', models.DateTimeField()),
                ('contactPerson', models.CharField(max_length=100)),
                ('contactNumber', models.PositiveBigIntegerField()),
                ('marketValue', models.IntegerField()),
                ('lifts', models.IntegerField()),
                ('brokerage', models.FloatField()),
                ('incentive', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('value', models.FloatField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CarpetArea', models.IntegerField()),
                ('price', models.IntegerField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='home_API.project')),
                ('unit', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='home_API.units')),
            ],
        ),
    ]
