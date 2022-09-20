# Generated by Django 3.0.6 on 2021-07-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0103_auto_20210708_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_five_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_four_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_one_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_seven_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_six_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_three_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h12_x02_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h12_x02_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h23_x03_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h23_x03_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h31_x01_ttr',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_h31_x01_ttr_error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='testsheet',
            name='tap_two_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
    ]
