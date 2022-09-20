# Generated by Django 3.0.6 on 2022-04-25 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0169_type_is_bus_resistance'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='interrupting_capacity',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=25, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='interrupting_voltage',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=25, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='system_voltage',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=25, null=True),
        ),
    ]
