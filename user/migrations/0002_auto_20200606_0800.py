# Generated by Django 3.0.7 on 2020-06-06 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='type',
            field=models.CharField(max_length=200),
        ),
    ]
