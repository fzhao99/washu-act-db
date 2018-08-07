# Generated by Django 2.1 on 2018-08-06 18:42

from django.conf import settings
from django.db import migrations, models
import hello.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0009_data_type_collection_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_type_collection',
            name='admins',
        ),
        migrations.AddField(
            model_name='data_type_collection',
            name='authorized_contributors',
            field=models.ManyToManyField(default=hello.models.get_all_users, related_name='auth_contributors', to=settings.AUTH_USER_MODEL),
        ),
    ]