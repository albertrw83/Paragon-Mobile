# Generated by Django 3.0.6 on 2020-10-28 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0069_auto_20201027_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
