# Generated by Django 3.0.7 on 2020-06-06 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20191019_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
    ]
