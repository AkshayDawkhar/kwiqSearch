# Generated by Django 4.2.3 on 2024-09-04 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_alter_employee_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='locality',
            field=models.CharField(blank=True, choices=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South'), ('central', 'Central')], max_length=100, null=True),
        ),
    ]