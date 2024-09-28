# Generated by Django 4.2.3 on 2024-09-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_alter_employee_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='user_type',
            field=models.CharField(blank=True, choices=[('CEO', 'CEO'), ('Manager', 'Manager'), ('LocalityManager', 'Locality Manager'), ('Caller', 'Caller'), ('Visitor', 'Visitor'), ('VisitorCaller', 'Visitor and Caller')], max_length=100, null=True),
        ),
    ]