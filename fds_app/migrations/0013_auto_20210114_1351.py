# Generated by Django 3.1.3 on 2021-01-14 12:51

from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    dependencies = [
        ('fds_app', '0012_auto_20210114_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fds_app.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='post_images',
            field=ImageField(default='', upload_to='post_images'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]
