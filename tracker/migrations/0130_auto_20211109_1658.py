# Generated by Django 3.0.6 on 2021-11-09 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0129_auto_20211109_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='oil_capacity',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
    ]
