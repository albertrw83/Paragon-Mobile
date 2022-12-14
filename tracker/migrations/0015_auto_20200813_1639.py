# Generated by Django 3.0.6 on 2020-08-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_auto_20200813_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='site_considerations',
        ),
        migrations.AddField(
            model_name='job',
            name='grounding_clamp_style',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='grounding_cluster_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='grounding_wire_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_40cal_protection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_8cal_protection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_fr_clothes',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_grounding_cluster',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_h2s_monitor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_hardhat',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_harness',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_insulated_gloves',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_mv_voltage_detector',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='is_safety_glasses',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_safety_gloves',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_safety_shoes',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_safety_vest',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='site_navigation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
