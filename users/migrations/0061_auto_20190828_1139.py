# Generated by Django 2.2.1 on 2019-08-28 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0060_auto_20190828_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='category',
            field=models.CharField(choices=[('Arts', 'Arts & Entertainment'), ('Industry', 'Industry'), ('Innovation', 'Innovation & Tech'), ('Life', 'Life'), ('Society', 'Society'), ('Miscellaneous', 'Miscellaneous')], max_length=100),
        ),
    ]
