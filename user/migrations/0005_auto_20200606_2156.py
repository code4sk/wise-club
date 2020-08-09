# Generated by Django 3.0.7 on 2020-06-06 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200606_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='best_quote',
            field=models.CharField(max_length=720, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='fav_books',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='interests',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='shelf_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]