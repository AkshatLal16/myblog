# Generated by Django 2.2.1 on 2019-08-13 05:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20190810_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 13, 5, 36, 26, 529824, tzinfo=utc)),
        ),
    ]
