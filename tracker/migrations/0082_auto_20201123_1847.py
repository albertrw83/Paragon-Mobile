# Generated by Django 3.0.6 on 2020-11-24 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0081_job_job_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='quote_default',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='type',
            name='quote_default',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
