# Generated by Django 3.0.5 on 2020-05-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accum_articles', '0004_auto_20200523_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptopbattery',
            name='manufacturer',
            field=models.CharField(choices=[('NoName', 'Unknown'), ('Hewlett Packard', 'HP'), ('ACER', 'ACER')], default='NoName', max_length=16),
        ),
    ]
