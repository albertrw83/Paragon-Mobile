# Generated by Django 3.0.6 on 2022-04-25 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0170_auto_20220424_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='is_dc_system_voltage',
            field=models.BooleanField(default=False),
        ),
    ]
