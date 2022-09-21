# Generated by Django 3.0.6 on 2020-10-16 04:58

from django.db import migrations, models
import django.db.models.deletion
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0065_auto_20201014_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_file', models.FileField(blank=True, null=True, upload_to=tracker.models.equipment_folder_path)),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='tracker.Equipment')),
            ],
        ),
    ]