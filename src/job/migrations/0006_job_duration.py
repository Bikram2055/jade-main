# Generated by Django 3.2.12 on 2023-02-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_remove_job_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='duration',
            field=models.DateField(null=True),
        ),
    ]
