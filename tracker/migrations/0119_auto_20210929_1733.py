# Generated by Django 3.0.6 on 2021-09-29 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0118_typeteststandards_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeteststandards',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_test_standard', to='tracker.UserProperties'),
        ),
    ]
