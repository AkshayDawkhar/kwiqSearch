# Generated by Django 4.2.3 on 2023-08-03 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_API', '0002_alter_searchfilter_startbudget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchfilter',
            name='startCarpetArea',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='searchfilter',
            name='stopCarpetArea',
            field=models.FloatField(),
        ),
    ]
