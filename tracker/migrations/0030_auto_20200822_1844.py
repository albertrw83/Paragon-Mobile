# Generated by Django 3.0.6 on 2020-08-22 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0029_auto_20200822_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='recommended_test_equipment',
            new_name='type_test_equipment',
        ),
    ]