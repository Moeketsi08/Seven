# Generated by Django 3.1.14 on 2024-10-14 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20241015_0014'),
        ('center_manager', '0002_auto_20241005_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center', to='address.address')),
            ],
        ),
        migrations.CreateModel(
            name='CenterManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surnname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_managers', to='address.address')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='reports/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='center_manager.center')),
                ('center_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='center_manager.centermanager')),
            ],
        ),
        migrations.AddField(
            model_name='center',
            name='center_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centers', to='center_manager.centermanager'),
        ),
    ]
