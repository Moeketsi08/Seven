# Generated by Django 5.1.3 on 2025-01-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0011_auto_20241031_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='SAT', max_length=9),
        ),
    ]
