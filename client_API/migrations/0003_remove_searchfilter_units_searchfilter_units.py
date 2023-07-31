# Generated by Django 4.2.3 on 2023-07-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_API', '0016_units_alter_unit_unit'),
        ('client_API', '0002_remove_searchfilter_area_searchfilter_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchfilter',
            name='units',
        ),
        migrations.AddField(
            model_name='searchfilter',
            name='units',
            field=models.ManyToManyField(to='home_API.units'),
        ),
    ]