# Generated by Django 2.2.6 on 2019-10-17 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20191017_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='body',
            field=models.TextField(null=True),
        ),
    ]
