# Generated by Django 3.0.6 on 2020-08-25 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0034_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproperties',
            name='equipment_supported',
        ),
        migrations.AddField(
            model_name='userproperties',
            name='equipment_type_supported',
            field=models.ManyToManyField(blank=True, related_name='equipment_type_supported', to='tracker.Type'),
        ),
    ]
