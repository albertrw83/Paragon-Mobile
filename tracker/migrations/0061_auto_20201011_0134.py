# Generated by Django 3.0.6 on 2020-10-11 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0060_auto_20201011_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='test_sheet',
            new_name='test_results',
        ),
    ]
