# Generated by Django 2.1 on 2018-08-07 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0014_auto_20180807_0143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data_type_collection',
            old_name='authorized_admins',
            new_name='admins',
        ),
    ]
