# Generated by Django 3.0.6 on 2020-08-12 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_remove_job_job_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='location_details',
        ),
        migrations.RemoveField(
            model_name='job',
            name='ppe_requirements',
        ),
    ]
