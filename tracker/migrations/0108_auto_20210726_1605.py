# Generated by Django 3.0.6 on 2021-07-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0107_auto_20210726_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='contact_resistance_a_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='contact_resistance_b_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='contact_resistance_c_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ln_to_ld_a_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ln_to_ld_b_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ln_to_ld_c_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_gr_a_g_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_gr_b_g_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_gr_c_g_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_ph_a_b_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_ph_b_c_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='insulation_resistance_ph_to_ph_c_a_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
