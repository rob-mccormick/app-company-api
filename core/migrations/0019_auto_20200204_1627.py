# Generated by Django 3.0.1 on 2020-02-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200204_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='specialism',
        ),
        migrations.AddField(
            model_name='job',
            name='specialism',
            field=models.ManyToManyField(to='core.JobMap'),
        ),
    ]
