# Generated by Django 3.2 on 2022-06-17 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0004_subfooterkeywordmodel_subfooterlongtailkeywordmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FooterLongTailKeywordModel',
            new_name='LongTailFooterKeywordModel',
        ),
        migrations.RenameModel(
            old_name='SubFooterLongTailKeywordModel',
            new_name='LongTailSubFooterKeywordModel',
        ),
    ]
