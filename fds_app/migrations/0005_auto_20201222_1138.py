# Generated by Django 3.1.3 on 2020-12-22 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0004_auto_20201222_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='date_of_registration',
            field=models.DateField(default='2020-12-22'),
        ),
    ]
