# Generated by Django 3.0.6 on 2020-08-14 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0019_auto_20200813_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='nav_link',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
