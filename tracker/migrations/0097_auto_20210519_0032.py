# Generated by Django 3.0.6 on 2021-05-19 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0096_auto_20210518_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
