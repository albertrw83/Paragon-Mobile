# Generated by Django 3.0.6 on 2020-08-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0030_auto_20200822_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='type_test_equipment',
            field=models.ManyToManyField(blank=True, related_name='type_test_equipment', to='tracker.TestEquipment'),
        ),
    ]
