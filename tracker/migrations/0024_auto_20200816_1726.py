# Generated by Django 3.0.6 on 2020-08-16 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_auto_20200816_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='harness',
        ),
        migrations.AddField(
            model_name='job',
            name='harness_lanyard',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='chairs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='tables',
            field=models.IntegerField(default=0),
        ),
    ]