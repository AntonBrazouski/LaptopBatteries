# Generated by Django 3.0.5 on 2020-05-23 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accum_articles', '0003_auto_20200517_1912'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Battery',
        ),
        migrations.DeleteModel(
            name='Description',
        ),
    ]