# Generated by Django 3.2 on 2023-04-18 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0029_alter_refreshcheck_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshcheck',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
