# Generated by Django 3.2 on 2023-05-03 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0036_linkofhousemodel_linkofworkmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listofhousemodel',
            name='date',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='listofworkmodel',
            name='date',
            field=models.CharField(default='', max_length=255),
        ),
    ]