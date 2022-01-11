# Generated by Django 3.2.8 on 2021-11-05 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_db', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='login',
        ),
        migrations.AddField(
            model_name='users',
            name='device_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='dt_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='dt_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(db_index=True, default='old@gmail.com', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='users',
            name='family',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='method',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 17, 31, 24, 688430)),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.TextField(null=True),
        ),
    ]
