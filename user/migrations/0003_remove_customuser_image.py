# Generated by Django 2.2.6 on 2019-10-17 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='image',
        ),
    ]
