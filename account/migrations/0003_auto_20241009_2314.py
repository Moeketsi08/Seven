# Generated by Django 3.1.14 on 2024-10-09 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20241005_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='employee_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('professor', 'Professor'), ('teacher', 'Teacher'), ('student', 'Student')], max_length=15),
        ),
    ]
