# Generated by Django 3.1.3 on 2020-12-22 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0002_auto_20201222_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='date_of_registration',
            field=models.DateField(),
        ),
    ]
