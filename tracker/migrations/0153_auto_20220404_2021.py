# Generated by Django 3.0.6 on 2022-04-05 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0152_auto_20220404_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='is_switchgear',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='type',
            name='is_switchgear',
            field=models.BooleanField(default=False),
        ),
    ]