# Generated by Django 3.0.6 on 2021-08-03 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0109_auto_20210728_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='ambient_temp_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='fluid_capacity_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_hi_g_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_hi_lo_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_lo_g_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='power_rating_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='temp_rise_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='testsheet',
            name='xfmr_class',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
