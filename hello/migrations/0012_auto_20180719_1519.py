# Generated by Django 2.0.7 on 2018-07-19 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0011_auto_20180719_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='active_group',
            name='views',
        ),
        migrations.AddField(
            model_name='submissions',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]