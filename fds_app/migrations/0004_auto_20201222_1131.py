# Generated by Django 3.1.3 on 2020-12-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0003_auto_20201222_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='date_of_registration',
            field=models.DateField(default='22/12/2020'),
        ),
    ]
