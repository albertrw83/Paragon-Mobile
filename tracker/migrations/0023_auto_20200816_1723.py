# Generated by Django 3.0.6 on 2020-08-16 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0022_auto_20200816_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='diesel',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='gasoline',
            field=models.IntegerField(default=0),
        ),
    ]
