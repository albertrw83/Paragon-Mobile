# Generated by Django 3.0.6 on 2022-04-13 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0159_testsheet_operating_voltage'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='is_dc_operating_voltage',
            field=models.BooleanField(default=False),
        ),
    ]
