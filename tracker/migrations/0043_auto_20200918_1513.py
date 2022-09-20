# Generated by Django 3.0.6 on 2020-09-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0042_auto_20200831_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='type_test_equipment',
            new_name='mandatory_type_test_equipment',
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='testequipment',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
