# Generated by Django 2.2.6 on 2019-10-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_auto_20191016_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
    ]
