# Generated by Django 3.0.6 on 2022-04-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0168_testsheet_bus_contact_resistance_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='is_bus_resistance',
            field=models.BooleanField(default=False),
        ),
    ]
