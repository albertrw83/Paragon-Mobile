# Generated by Django 3.0.6 on 2020-08-26 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0038_auto_20200826_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='template',
            new_name='equipment_type',
        ),
    ]
