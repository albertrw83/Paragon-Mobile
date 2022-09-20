# Generated by Django 3.0.6 on 2021-06-17 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0097_auto_20210519_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_complete', models.BooleanField(default=False)),
                ('date_tested', models.DateField()),
                ('testers', models.CharField(blank=True, max_length=256, null=True)),
                ('date_manufactured', models.DateField()),
                ('control_voltage', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('trip_coil_voltage', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_ph_test_voltage', models.IntegerField(blank=True, null=True)),
                ('insulation_resistance_ph_to_ph_a_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_ph_b_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_ph_c_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ln_to_ld_test_voltage', models.IntegerField(blank=True, null=True)),
                ('insulation_resistance_ln_to_ld_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ln_to_ld_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ln_to_ld_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_gr_test_voltage', models.IntegerField(blank=True, null=True)),
                ('insulation_resistance_ph_to_gr_a_g', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_gr_b_g', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('insulation_resistance_ph_to_gr_c_g', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('contact_resistance_current', models.IntegerField(blank=True, null=True)),
                ('contact_resistance_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('contact_resistance_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('contact_resistance_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('control_wiring_insulation_resistance', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('frame_size', models.IntegerField(blank=True, null=True)),
                ('mount_style', models.CharField(blank=True, max_length=128, null=True)),
                ('trip_unit_model', models.TextField(blank=True, null=True)),
                ('trip_unit_manufacturer', models.IntegerField(blank=True, null=True)),
                ('trip_unit_serial_number', models.IntegerField(blank=True, null=True)),
                ('trip_unit_rating_plug', models.IntegerField(blank=True, null=True)),
                ('trip_unit_curve', models.TextField(blank=True, null=True)),
                ('trip_unit_phase_ct_high', models.IntegerField(blank=True, null=True)),
                ('trip_unit_phase_ct_low', models.IntegerField(blank=True, null=True)),
                ('settings_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('settings_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('is_primary_injection', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_setting_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_testamps_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_testamps_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_testamps_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_xpu_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_xpu_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_xpu_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pi_xpu_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('a_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('b_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('c_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('min_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_af_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_ltpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_ltd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_stpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_std', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_inst', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_gfpu', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('max_al_gfd', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_pu_a', models.IntegerField(blank=True, null=True)),
                ('si_pu_b', models.IntegerField(blank=True, null=True)),
                ('si_pu_c', models.IntegerField(blank=True, null=True)),
                ('si_lt_current_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_lt_current_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_lt_current_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_lt_d_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_lt_d_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_lt_d_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_current_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_current_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_current_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_d_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_d_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_st_d_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_inst_current_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_inst_current_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('si_inst_current_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('trip_device', models.TextField(blank=True, null=True)),
                ('operations_counter_af', models.IntegerField(blank=True, null=True)),
                ('operations_counter_al', models.IntegerField(blank=True, null=True)),
                ('heaters_operational', models.BooleanField(default=True)),
                ('hipot_ptp_ab', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ptp_bc', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ptp_ca', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ltl_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ltl_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ltl_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ptg_a', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ptg_b', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('hipot_ptg_c', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('power_rating', models.IntegerField(blank=True, null=True)),
                ('primary_winding_config', models.CharField(blank=True, max_length=64, null=True)),
                ('secondary_winding_config', models.CharField(blank=True, max_length=64, null=True)),
                ('primary_voltage', models.IntegerField(blank=True, null=True)),
                ('secondary_voltage', models.IntegerField(blank=True, null=True)),
                ('temp_rise', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('impedance', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('impedance_at', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('xfmr_class', models.IntegerField(blank=True, null=True)),
                ('ambient_temp', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_qty', models.IntegerField(blank=True, null=True)),
                ('tap_position', models.IntegerField(blank=True, null=True)),
                ('wr_h1_h2', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('wr_h2_h3', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('wr_h3_h1', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('wr_x0_x1', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('wr_x0_x2', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('wr_x0_x3', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_one_volts', models.IntegerField(blank=True, null=True)),
                ('tap_one_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_one_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_one_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_one_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_two_volts', models.IntegerField(blank=True, null=True)),
                ('tap_two_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_two_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_two_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_two_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_three_volts', models.IntegerField(blank=True, null=True)),
                ('tap_three_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_three_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_three_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_three_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_four_volts', models.IntegerField(blank=True, null=True)),
                ('tap_four_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_four_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_four_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_four_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_five_volts', models.IntegerField(blank=True, null=True)),
                ('tap_five_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_five_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_five_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_five_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_six_volts', models.IntegerField(blank=True, null=True)),
                ('tap_six_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_six_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_six_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_six_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_seven_volts', models.IntegerField(blank=True, null=True)),
                ('tap_seven_ratio', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_seven_h12_x02', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_seven_h23_x03', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('tap_seven_h31_x01', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('is_oil_sample_required', models.BooleanField(default=True)),
                ('tap_af', models.IntegerField(blank=True, null=True)),
                ('tap_al', models.IntegerField(blank=True, null=True)),
                ('fluid_type', models.TextField(blank=True, null=True)),
                ('fluid_capacity', models.TextField(blank=True, null=True)),
                ('liquid_level', models.TextField(blank=True, null=True)),
                ('liquid_temp', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('liquid_temp_units', models.CharField(blank=True, max_length=64, null=True)),
                ('winding_temp', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('winding_temp_units', models.CharField(blank=True, max_length=64, null=True)),
                ('pressure', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('pressure_units', models.CharField(blank=True, max_length=64, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('weight_units', models.CharField(blank=True, max_length=64, null=True)),
                ('eq_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sheet_model', to='tracker.Model')),
                ('eq_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sheet_type', to='tracker.Type')),
            ],
        ),
    ]
