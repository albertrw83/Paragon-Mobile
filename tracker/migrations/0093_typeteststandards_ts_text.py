# Generated by Django 3.0.6 on 2021-05-13 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0092_typeteststandards'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeteststandards',
            name='ts_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]