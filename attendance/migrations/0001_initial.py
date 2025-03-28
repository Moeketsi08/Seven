# Generated by Django 5.1.1 on 2024-10-02 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classregistration')),
                ('learner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='academic.learner')),
            ],
            options={
                'unique_together': {('learner', 'date')},
            },
        ),
    ]
