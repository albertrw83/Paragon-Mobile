# Generated by Django 3.0.6 on 2022-03-13 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0149_auto_20220313_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsheet',
            name='cable_voltage_rating',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='testsheet',
            name='operating_cable_voltage',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
    ]
