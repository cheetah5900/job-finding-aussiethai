# Generated by Django 3.2 on 2023-04-14 02:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0026_auto_20230414_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listofhousemodel',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='listofworkmodel',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
