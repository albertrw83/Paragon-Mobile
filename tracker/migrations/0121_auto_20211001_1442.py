# Generated by Django 3.0.6 on 2021-10-01 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0120_equipment_is_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=16, null=True),
        ),
    ]
