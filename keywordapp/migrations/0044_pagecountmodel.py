# Generated by Django 3.2 on 2023-07-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0043_auto_20230703_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageCountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
        ),
    ]
