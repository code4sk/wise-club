# Generated by Django 2.2.6 on 2019-10-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.URLField(),
        ),
    ]
