# Generated by Django 3.0.6 on 2021-03-02 07:15

from django.db import migrations, models
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0087_auto_20210227_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_file', models.FileField(blank=True, max_length=500, null=True, upload_to=tracker.models.feedback_file_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userproperties',
            name='is_fsr',
            field=models.BooleanField(default=True),
        ),
    ]
