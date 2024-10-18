# Generated by Django 3.1.14 on 2024-10-17 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center_manager', '0005_centermanager_user'),
        ('learner', '0010_learner_center'),
        ('teacher', '0005_auto_20241017_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='center_manager.center'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='learners',
            field=models.ManyToManyField(related_name='classrooms', to='learner.Learner'),
        ),
    ]
