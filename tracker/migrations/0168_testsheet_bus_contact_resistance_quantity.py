# Generated by Django 3.0.6 on 2022-04-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0167_auto_20220422_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='bus_contact_resistance_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
