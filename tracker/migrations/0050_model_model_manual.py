# Generated by Django 3.0.6 on 2020-09-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0049_auto_20200925_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='model_manual',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
