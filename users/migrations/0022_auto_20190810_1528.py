# Generated by Django 2.2.1 on 2019-08-10 09:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20190808_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 10, 9, 58, 26, 767154, tzinfo=utc)),
        ),
    ]