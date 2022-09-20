# Generated by Django 3.0.6 on 2020-08-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0040_auto_20200826_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='equipment_answers',
        ),
        migrations.RemoveField(
            model_name='model',
            name='manual_folder',
        ),
        migrations.AddField(
            model_name='type',
            name='type_test_guide',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='model_id',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
