# Generated by Django 3.2 on 2023-07-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0041_auto_20230514_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnwantedList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
            ],
        ),
    ]