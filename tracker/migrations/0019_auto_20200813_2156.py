# Generated by Django 3.0.6 on 2020-08-14 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0018_auto_20200813_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='online_job_folder',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
