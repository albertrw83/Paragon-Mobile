# Generated by Django 3.0.6 on 2022-03-07 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0138_equipmentlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentlink',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_eq_link', to=settings.AUTH_USER_MODEL),
        ),
    ]
