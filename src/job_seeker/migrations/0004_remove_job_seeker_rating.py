# Generated by Django 3.2.12 on 2023-02-08 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0003_delete_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_seeker',
            name='rating',
        ),
    ]