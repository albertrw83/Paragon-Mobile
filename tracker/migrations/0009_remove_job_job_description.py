# Generated by Django 3.0.6 on 2020-08-12 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_auto_20200811_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_description',
        ),
    ]
