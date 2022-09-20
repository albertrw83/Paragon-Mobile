# Generated by Django 3.0.6 on 2020-07-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_template_equipment_help'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='equipment_help',
        ),
        migrations.AddField(
            model_name='userproperties',
            name='equipment_supported',
            field=models.ManyToManyField(blank=True, related_name='equipment_supported', to='tracker.Template'),
        ),
        migrations.AddField(
            model_name='userproperties',
            name='help_username',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='userproperties',
            name='is_support',
            field=models.BooleanField(default=False),
        ),
    ]
