# Generated by Django 3.0.6 on 2020-08-22 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0027_auto_20200822_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='equipment_questions',
        ),
    ]
