# Generated by Django 3.0.6 on 2020-11-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0084_auto_20201123_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentfolder',
            name='file_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='jobfolder',
            name='file_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='jobsitefolder',
            name='file_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='modelfolder',
            name='file_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='typefolder',
            name='file_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]