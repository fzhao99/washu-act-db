# Generated by Django 2.0.7 on 2018-07-19 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0010_data_type_collection_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_type_collection',
            name='views',
        ),
        migrations.AddField(
            model_name='active_group',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
