# Generated by Django 3.1.3 on 2020-12-21 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='members',
            old_name='Gender',
            new_name='gender',
        ),
        migrations.AlterField(
            model_name='members',
            name='phone_number',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='members',
            name='whatsapp_number',
            field=models.CharField(max_length=13),
        ),
    ]
