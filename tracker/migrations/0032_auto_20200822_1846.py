# Generated by Django 3.0.6 on 2020-08-22 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0031_auto_20200822_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='cloud_link',
            new_name='type_folder',
        ),
    ]