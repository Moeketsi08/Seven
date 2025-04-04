# Generated by Django 3.1.14 on 2024-10-17 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center_manager', '0005_centermanager_user'),
        ('learner', '0009_auto_20241017_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='center',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='learners', to='center_manager.center'),
            preserve_default=False,
        ),
    ]
