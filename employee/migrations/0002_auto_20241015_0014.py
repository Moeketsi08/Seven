# Generated by Django 3.1.14 on 2024-10-14 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeaddressinfo',
            name='district',
        ),
        migrations.RemoveField(
            model_name='employeeaddressinfo',
            name='union',
        ),
        migrations.RemoveField(
            model_name='employeeaddressinfo',
            name='upazilla',
        ),
        migrations.RemoveField(
            model_name='employeejobinfo',
            name='department',
        ),
        migrations.RemoveField(
            model_name='employeejobinfo',
            name='job_designation',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='address',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='education',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='job',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='training',
        ),
        migrations.DeleteModel(
            name='EducationInfo',
        ),
        migrations.DeleteModel(
            name='EmployeeAddressInfo',
        ),
        migrations.DeleteModel(
            name='EmployeeJobInfo',
        ),
        migrations.DeleteModel(
            name='ExperienceInfo',
        ),
        migrations.DeleteModel(
            name='PersonalInfo',
        ),
        migrations.DeleteModel(
            name='TrainingInfo',
        ),
    ]
