# Generated by Django 3.2 on 2023-04-14 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0025_templinkofhousemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listofhousemodel',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='listofworkmodel',
            name='date',
            field=models.DateField(),
        ),
    ]