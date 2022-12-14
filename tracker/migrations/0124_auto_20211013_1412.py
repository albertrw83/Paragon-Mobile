# Generated by Django 3.0.6 on 2021-10-13 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0123_auto_20211003_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsheet',
            name='eq',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sheet_eq', to='tracker.Equipment'),
        ),
        migrations.AlterField(
            model_name='type',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=16, null=True),
        ),
    ]
