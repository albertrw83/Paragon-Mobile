# Generated by Django 3.0.6 on 2020-10-16 18:35

from django.db import migrations, models
import django.db.models.deletion
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0066_equipmentfolder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_file', models.FileField(blank=True, null=True, upload_to=tracker.models.model_folder_path)),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='tracker.Model')),
            ],
        ),
    ]
