# Generated by Django 3.1.14 on 2024-10-09 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_delete_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Shift',
        ),
    ]
