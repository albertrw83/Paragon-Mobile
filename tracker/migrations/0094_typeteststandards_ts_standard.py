# Generated by Django 3.0.6 on 2021-05-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0093_typeteststandards_ts_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeteststandards',
            name='ts_standard',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
