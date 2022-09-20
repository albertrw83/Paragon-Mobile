# Generated by Django 3.0.6 on 2022-03-09 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0139_equipmentlink_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='cable_withstand_units',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='duration_per_step',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_bend_radius',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_cable_data_specs_match',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_cable_dc_test',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_cable_jacket_insulation_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_compression_match',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_connection_verification',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_fireproofing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_id_arrangments_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_no_physical_damage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_shield_supports_terminations',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='is_window_ct_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='max_test_voltage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='shield_continuity_a',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='shield_continuity_b',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='shield_continuity_c',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='voltage_step_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testsheet',
            name='cable_insulation_thickness',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='testsheet',
            name='is_cable_shielded',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='CableTestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_result_key', models.IntegerField(blank=True, null=True)),
                ('time', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('test_voltage', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('phase_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('phase_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('phase_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('notes', models.CharField(blank=True, max_length=256, null=True)),
                ('test_sheet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cable_test_data', to='tracker.Model')),
            ],
        ),
    ]
