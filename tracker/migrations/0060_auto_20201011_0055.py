# Generated by Django 3.0.6 on 2020-10-11 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0059_auto_20201010_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='model_manual',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]
