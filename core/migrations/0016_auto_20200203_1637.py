# Generated by Django 3.0.1 on 2020-02-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200203_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companychatbot',
            name='benefits_message',
        ),
        migrations.RemoveField(
            model_name='companychatbot',
            name='benefits_url',
        ),
        migrations.AddField(
            model_name='benefit',
            name='benefits_message',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='benefit',
            name='benefits_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
