# Generated by Django 3.2 on 2022-08-30 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0173_auto_20220512_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='change_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='change_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
