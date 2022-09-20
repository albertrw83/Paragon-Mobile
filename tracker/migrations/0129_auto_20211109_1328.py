# Generated by Django 3.0.6 on 2021-11-09 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0128_maintevent_maintfile_maintnotes_well_wellnotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='well',
            name='nav_link',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
