# Generated by Django 3.0.1 on 2020-01-01 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CbJobsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatbot_user_id', models.CharField(max_length=60)),
                ('date_time', models.DateTimeField()),
                ('specialism_search', models.CharField(max_length=100)),
                ('location_search', models.CharField(max_length=60)),
                ('role_type_search', models.CharField(max_length=100)),
                ('found_job', models.NullBooleanField()),
                ('saw_benefits', models.NullBooleanField()),
                ('saw_company_video', models.NullBooleanField()),
                ('saw_job_video', models.NullBooleanField()),
                ('add_to_pipeline', models.NullBooleanField()),
                ('joined_pipeline', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
            ],
            options={
                'verbose_name_plural': 'Chatbot job data',
            },
        ),
    ]
