# Generated by Django 3.0.6 on 2020-08-31 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0041_auto_20200828_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='test_sheet',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='type_folder',
            field=models.URLField(blank=True, null=True),
        ),
    ]