# Generated by Django 3.1.3 on 2021-01-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0008_auto_20210108_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date_of_transaction',
            field=models.DateTimeField(),
        ),
    ]
