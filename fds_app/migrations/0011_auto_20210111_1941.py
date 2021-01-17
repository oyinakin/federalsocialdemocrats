# Generated by Django 3.1.3 on 2021-01-11 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0010_auto_20210110_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='date_of_registration',
            field=models.DateField(default='2021-01-11'),
        ),
        migrations.AlterField(
            model_name='members',
            name='email',
            field=models.EmailField(max_length=200, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
