# Generated by Django 3.1.14 on 2024-10-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0009_auto_20241015_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(choices=[('10', 'Grade 10'), ('11', 'Grade 11'), ('12', 'Grade 12')], default='10', max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject',
            field=models.CharField(choices=[('Mathematics', 'Mathematics'), ('Mathematics Exam', 'Mathematics Examination'), ('Physical Science', 'Physical Science'), ('Physical Science Exam', 'Physical Science Examination')], default='Mathematics', max_length=21, unique=True),
        ),
    ]
