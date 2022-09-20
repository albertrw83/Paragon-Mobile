# Generated by Django 3.0.6 on 2020-10-09 01:48

from django.db import migrations, models
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0054_auto_20201006_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='test_sheet',
            field=models.FileField(blank=True, null=True, upload_to=tracker.models.upload_test_results_path),
        ),
        migrations.AlterField(
            model_name='type',
            name='test_sheet',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='type',
            name='type_test_guide',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]
