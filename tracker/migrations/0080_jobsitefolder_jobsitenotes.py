# Generated by Django 3.0.6 on 2020-11-21 21:09

from django.db import migrations, models
import django.db.models.deletion
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0079_jobsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSiteNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('jobsite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_jobsite', to='tracker.JobSite')),
            ],
        ),
        migrations.CreateModel(
            name='JobSiteFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobsite_file', models.FileField(blank=True, max_length=500, null=True, upload_to=tracker.models.jobsite_folder_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('jobsite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobsite', to='tracker.JobSite')),
            ],
        ),
    ]
