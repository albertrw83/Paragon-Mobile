# Generated by Django 3.0.6 on 2021-11-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0131_maintevent_well'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintevent',
            name='hours',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
    ]
