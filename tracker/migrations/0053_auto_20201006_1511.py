# Generated by Django 3.0.6 on 2020-10-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0052_auto_20201006_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='grounding_wire_size',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]