# Generated by Django 3.0.6 on 2020-08-13 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_auto_20200811_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='end_date',
            field=models.DateField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_date',
            field=models.DateField(blank=True, max_length=64, null=True),
        ),
    ]